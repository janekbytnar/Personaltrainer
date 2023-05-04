import datetime

import stripe
import djstripe
import json

from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from djstripe.models import Product, Price
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import Plans, UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from djangoProject1 import settings

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

@receiver(post_save, sender=Plans)
def create_stripe_product(sender, instance, created, **kwargs):
    if created:
        try:
            product = stripe.Product.create(
                name=instance.name,
                description=instance.description
            )
            stripe.Price.create(
                product=product.id,
                unit_amount=instance.priceMonthly * 100,  # Stripe oczekuje ceny w centach
                currency='gbp',
                recurring={'interval': 'month'}
            )
            stripe.Price.create(
                product=product.id,
                unit_amount=instance.priceYearly * 100,  # Stripe oczekuje ceny w centach
                currency='gbp',
                recurring={'interval': 'year'}
            )
            instance.stripe_product_id = product.id
            instance.save()
        except stripe.error.StripeError as e:
            print(f"Stripe error: {e}")


@method_decorator(login_required, name='dispatch')
class CheckoutView(TemplateView):
    template_name = "subscription/checkout.html"

    def get(self, request, *args, **kwargs):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        if user_profile.active:
            return HttpResponseRedirect('/plan/')
        else:
            return super(CheckoutView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        products = Product.objects.all()
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context.update({
            "products": products,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_TEST_PUBLIC_KEY
        })
        return context


@method_decorator(login_required, name='dispatch')
class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:

            data = json.loads(request.body)
            payment_method = data['payment_method']

            payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
            djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)

            # This creates a new Customer and attaches the PaymentMethod in one API call.
            customer = stripe.Customer.create(
                payment_method=payment_method,
                email=request.user.email,
                invoice_settings={
                    'default_payment_method': payment_method
                }
            )

            djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)
            request.user.customer = djstripe_customer

            # At this point, associate the ID of the Customer object with your
            # own internal representation of a customer, if you have one.
            # print(customer)

            # Subscribe the user to the subscription created
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[
                    {
                        "price": data["price_id"],
                    },
                ],
                expand=["latest_invoice.payment_intent"]
            )

            djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)

            request.user.subscription = djstripe_subscription
            request.user.customer = djstripe_customer
            request.user.save()

            # creating the intent
            price = Price.objects.get(id=self.kwargs["pk"])
            intent = stripe.PaymentIntent.create(
                amount=price.unit_amount,
                currency='gbp',
                customer=customer['id'],
                description="PT PT",
                metadata={
                    "price_id": price.id,
                    "subscription_id": subscription.id
                }
            )

            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
@require_POST
def update_user_profile(request):
    data = json.loads(request.body)
    payment_id = data.get('payment_id')
    user_id = data.get('user_id')
    plan_id = data.get('plan_id')


    # tutaj zweryfikuj płatność za pomocą Stripe API

    # jeśli płatność jest poprawna, zaktualizuj profil użytkownika
    user = get_object_or_404(User, id=user_id)
    plan = get_object_or_404(Plans, name=plan_id)

    subscription = get_subscription_info(payment_id)


    user_profile, created = UserProfile.objects.get_or_create(user=user)
    user_profile.plan = plan
    user_profile.startDate = datetime.datetime.fromtimestamp(
        subscription['current_period_start']
    )
    user_profile.endDate = end_date = datetime.datetime.fromtimestamp(
        subscription['current_period_end']
     )
    user_profile.nextPlan = plan
    user_profile.active = True
    user_profile.subscription_id = subscription['id']
    user_profile.save()

    return JsonResponse({'status': 'success'})

def get_subscription_info(payment_intent_id):
    try:
        # Pobierz szczegóły PaymentIntent

        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        # Pobierz identyfikator subskrypcji z metadanych PaymentIntent
        subscription_id = payment_intent.metadata.get('subscription_id')

        # Pobierz szczegóły subskrypcji
        subscription = stripe.Subscription.retrieve(subscription_id)


        return subscription

    except stripe.error.StripeError as e:
        print(f"Stripe error: {e}")
        return None

class CancelSubscription(View):
    def post(self, request, *args, **kwargs):

        # Pobierz subskrypcję użytkownika
        user_profile = UserProfile.objects.get(user=request.user)

        if user_profile.subscription_id is not None:
            try:
                # Anuluj subskrypcję na koniec okresu rozliczeniowego
                subscription = stripe.Subscription.modify(
                    user_profile.subscription_id,
                    cancel_at_period_end=True,
                )

                # Zaktualizuj status subskrypcji w modelu UserProfile
                user_profile.active = False
                user_profile.save()

                messages.success(request, "Twoja subskrypcja została anulowana. Będzie aktywna do końca bieżącego okresu rozliczeniowego.")
            except stripe.error.StripeError as e:
                messages.error(request, "Wystąpił błąd podczas anulowania subskrypcji. Spróbuj ponownie później.")
        else:
            messages.error(request, "Nie masz aktywnej subskrypcji do anulowania.")

        return redirect('/')

@login_required
def success(request):
    return render(request, 'subscription/success.html')

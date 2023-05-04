from django.core.management.base import BaseCommand

from djangoProject1 import settings
from main.models import Plans
import stripe

secretKeyApi = settings.STRIPE_TEST_SECRET_KEY
class Command(BaseCommand):
    help = 'Add existing plans to Stripe'

    def handle(self, *args, **options):
        stripe.api_key = secretKeyApi
        plans = Plans.objects.filter(stripe_product_id__isnull=True)
        for plan in plans:
            try:
                product = stripe.Product.create(
                    name=plan.name,
                    description=plan.description
                )
                stripe.Price.create(
                    product=product.id,
                    unit_amount=plan.priceMonthly * 100,  # Stripe oczekuje ceny w centach
                    currency='gbp',
                    recurring={'interval': 'month'}
                )
                stripe.Price.create(
                    product=product.id,
                    unit_amount=plan.priceYearly * 100,  # Stripe oczekuje ceny w centach
                    currency='gbp',
                    recurring={'interval': 'year'}
                )
                plan.stripe_product_id = product.id
                plan.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully added plan {plan.name} to Stripe'))
            except stripe.error.StripeError as e:
                self.stdout.write(self.style.ERROR(f'Stripe error with plan {plan.name}: {e}'))

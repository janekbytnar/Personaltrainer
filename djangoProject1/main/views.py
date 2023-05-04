from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Plans, UserProfile
from .forms import MessageForm
from django.contrib.auth.decorators import login_required
import json
import stripe

# This is your test secret API key.
stripe.api_key = 'sk_test_51N2HaRBOMcxwrn2jMMKFmCnI9WGIVYhKM0YcydNwYnCTLcMr9nkWsPkN4tgdfy5fsPBxvUSSDyKKUI290uD2JV2400FNIPgRmY'





# Create your views here.

def index(response, plan):
    try:
        ls = Plans.objects.get(name=plan)
    except:
        url = reverse('home')  # Assuming the URL pattern name for the view is 'home'
        return HttpResponseRedirect(url)

    return render(response, "main/plan.html", {"ls": ls})


def home(response):
    return render(response, "main/home.html", {"name": "test"})


@login_required
def plan_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('/subscribe/checkout')

    if not user_profile.active:
        return redirect('/subscribe/checkout')

    if not user_profile.active:
        return redirect('/subscribe/checkout')
    ls = user_profile.plan
    workout = []
    for i in ls.workout_set.all():
        exercise = i.to_dict()
        exercise['yturl'] = i.exercise.video
        exercise['description'] = i.exercise.description.replace("\n", " ")
        workout.append(exercise)

    context = {
        'ls': ls,
        'data': json.dumps(workout)
    }

    return render(request, 'main/plan.html', context)

@login_required
def subscription(request):


    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('/subscribe/checkout')
    if not user_profile.active:
        return redirect('/subscribe/checkout')
    endDate = user_profile.endDate
    startDate = user_profile.startDate
    plan = Plans.objects.get(name=user_profile.plan)
    planName = plan.name
    priceMonthly = plan.priceMonthly
    priceYearly = plan.priceYearly
    numberOfDays = (endDate - startDate).days
    nextPlan = user_profile.nextPlan

    context = {
        'plan': plan,
        'priceMonthly': priceMonthly,
        'priceYearly': priceYearly,
        'numberOfDays': numberOfDays,
        'nextPayment': endDate,
        'nextPlan': nextPlan
    }
    if nextPlan is not None:
        if nextPlan.priceMonthly != plan.priceMonthly and nextPlan.priceYearly != plan.priceYearly:
            context['newPriceMonthly'] = nextPlan.priceMonthly
            context['newPriceYearly'] = nextPlan.priceYearly
    return render(request, 'main/subscription.html', context)


@login_required
def changePlan(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('/subscribe/checkout')

    if not user_profile.active:
        return redirect('/subscribe/checkout')
    ls = user_profile.plan
    pls = Plans.objects.all()
    plansList = [plan.to_dict() for plan in pls]
    context = {
        'currentSex': json.dumps({"currentSex": ls.sex}),
        'plan': ls,
        'plans': json.dumps(plansList)
    }
    if request.method == 'POST':
        plan_radio = request.POST.get('planRadio')
        if plan_radio:
            try:
                selectedNewPlan = Plans.objects.get(name=plan_radio)
                user_profile = UserProfile.objects.get(user=request.user)
                user_profile.nextPlan = selectedNewPlan
                user_profile.save()
                messages.success(request, 'Your plan has been updated!')
                return redirect('subscription')
            except UserProfile.DoesNotExist:
                messages.error(request, 'User profile does not exist.')
        else:
            messages.error(request, 'Please select a plan.')
            return redirect('changePlan')
    return render(request, 'main/changePlan.html', context)


def contact(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.user = request.user
            new_message.save()
            # tutaj możesz przekierować do innej strony albo wyrenderować ten sam widok z informacją o sukcesie
            return render(request, 'main/contact.html', {'form': form, 'message': "Message sent!"})
    else:
        form = MessageForm()
    return render(request, 'main/contact.html', {'form': form})

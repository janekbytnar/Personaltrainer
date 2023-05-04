from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import RegisterForm, EditForm


# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect("/plan")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            return redirect("/")
    else:
        form = RegisterForm()

    return render(request, "register/register.html", {"form": form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        editForm = EditForm(request.POST, instance=request.user)
        if editForm.is_valid():
            editForm.save()
            return redirect('myinfo')
    else:
        editForm = EditForm(instance=request.user)

    return render(request, 'register/update_profile.html', {"editForm": editForm})

@login_required
def change_password(request):
    if request.method == 'POST':
        passwordForm = PasswordChangeForm(data=request.POST, user=request.user)
        if passwordForm.is_valid():
            passwordForm.save()
            return redirect('myinfo')
    else:
        passwordForm = PasswordChangeForm(user=request.user)

    return render(request, 'register/change_password.html', {"passwordForm": passwordForm})

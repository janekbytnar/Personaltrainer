"""djangoProject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView

from register.views import register, edit_profile, change_password

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('myinfo/', edit_profile, name='myinfo'),
    path('myinfo/password/', change_password, name='change_password'),
    path('', include('main.urls')),
    path('', include("django.contrib.auth.urls")),
    path('subscribe/', include('subscription.urls'), name='subscribe'),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    re_path(r'^.*$', RedirectView.as_view(url='/', permanent=False)),
]

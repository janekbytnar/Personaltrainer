from django.urls import path
from . import views

urlpatterns = [
    path('plan/', views.plan_view, name='plan_view'),
    path("", views.home, name="home"),
    path('subscription/', views.subscription, name='subscription'),
    path("changePlan/", views.changePlan, name="changePlan"),
    path("contact/", views.contact, name="contact"),
]

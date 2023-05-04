from django.urls import path
from .views import CheckoutView, StripeIntentView, CancelSubscription
from . import views

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('create_subscription/<pk>/', StripeIntentView.as_view(), name='create_subscription'),
    path('update_user_profile/', views.update_user_profile, name='update_user_profile'),
    path('cancel-subscription/', CancelSubscription.as_view(), name='cancel_subscription'),
    path('success/', views.success, name='success'),

]

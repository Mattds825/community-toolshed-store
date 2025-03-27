from django.contrib import admin
from django.urls import path, include
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_success/<order_number>', views.checkout_success, name='checkout_success'),
    path('subscription_checkout/', views.subscription_checkout, name='subscription_checkout'),
    path('subscription_checkout_success/<subscription_number>', views.subscription_checkout_success, name='subscription_checkout_success'),
    path("cache_checkout_data/", views.cache_checkout_data, name="cache_checkout_data"),
    path("cache_subscription_checkout_data/", views.cache_subscription_checkout_data, name="cache_subscription_checkout_data"),
    path('wh/', webhook, name='webhook'),
]
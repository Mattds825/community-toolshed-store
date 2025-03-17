from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages 
from django.conf import settings

from profiles.models import UserProfile
from .forms import PaymentForm
from cart.contexts import cart_contents

import stripe

# Create your views here.


def checkout(request):
    
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    
    cart = request.session.get('cart', {})
    
    profile = get_object_or_404(UserProfile, user=request.user)
    form = PaymentForm(instance=profile)
    
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    
    if not cart:
        messages.error(request, "There's nothing in your cart at the moment")
        return redirect(reverse('products'))
    
    current_cart = cart_contents(request)
    total = current_cart['total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )
    
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')
    
    print(intent)
    
    template = 'checkout/checkout.html'
    context = {
        'form': form,
        'profile': profile,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    
    
    return render(request, template, context) 
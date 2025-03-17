from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages 

from profiles.models import UserProfile
from .forms import PaymentForm

# Create your views here.


def checkout(request):
    
    cart = request.session.get('cart', {})
    
    profile = get_object_or_404(UserProfile, user=request.user)
    form = PaymentForm(instance=profile)
    
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    
    if not cart:
        messages.error(request, "There's nothing in your cart at the moment")
        return redirect(reverse('products'))
    
    template = 'checkout/checkout.html'
    context = {
        'form': form,
        'profile': profile,
    }
    
    
    return render(request, template, context) 
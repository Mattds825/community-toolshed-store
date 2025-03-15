from django.shortcuts import render, redirect, reverse
from django.contrib import messages 

# Create your views here.


def checkout(request):
    
    cart = request.session.get('cart', {})
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    
    if not cart:
        messages.error(request, "There's nothing in your cart at the moment")
        return redirect(reverse('products'))
    
    
    return render(request, 'checkout/checkout.html') 
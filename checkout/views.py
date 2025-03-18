from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages 
from django.conf import settings

from profiles.models import UserProfile
from .forms import PaymentForm
from cart.contexts import cart_contents
from products.models import Item
from .models import Order, OrderItem
from profiles.models import UserProfile

import stripe

# Create your views here.


def checkout(request):
    """
    A view to return the checkout page
    handle the payment form submission
    """
    
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        
        form_data = {
            'full_name': request.POST['full_name'],
            'email_address': request.POST['email_address'],
            'phone_number': request.POST['phone_number'],            
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        
        order_form = PaymentForm(form_data)
        if order_form.is_valid(): 
            # order = order_form.save()
            order = Order(
                user_profile=UserProfile.objects.get(user=request.user),
                start_date=request.session.get('start_date'),
                end_date=request.session.get('end_date'),
            )
            order.save()
            for item_id, item_data in cart.items():
                try:
                    item = Item.objects.get(id=item_id)
                    order_line_item = OrderItem(
                            order=order,
                            item=item,
                            quantity=item_data,
                        )
                    order_line_item.save()
                except Item.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_cart'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. Please double check your information')
    else: 
        cart = request.session.get('cart', {})
        
        profile = None
        
        if request.user.is_authenticated:
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


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    # profile = get_object_or_404(UserProfile, user=order.user_profile)
    
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.user_profile.email_address}.')
    
    if 'cart' in request.session:
        del request.session['cart']
        
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }
    
    return render(request, template, context)
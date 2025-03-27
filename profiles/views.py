from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages

from .models import UserProfile
from checkout.models import Order
from .forms import UserProfileForm

# Create your views here.

def profile(request):
    """ Display the user's profile. """
    
    profile = get_object_or_404(UserProfile, user=request.user)
    current_subscription = None
    
    if profile.subscriptions.all():
        for subscription in profile.subscriptions.all():
            if subscription.start_date <= timezone.localdate() <= subscription.end_date:
                profile.active_subscription = True
                current_subscription = subscription
                break                
    else:
        profile.active_subscription = False
    
    form = UserProfileForm(instance=profile)
    
    print(request.user.email)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

    form = UserProfileForm(instance=profile)
    orders = profile.orders.all()
    
    template = 'profiles/profile.html'
    context = {
        'profile': profile,
        'form': form,
        'orders': orders,
        'only_message_text': True,
        'current_subscription': current_subscription,
    }
    
    return render(request, template, context)

def order_history(request, order_number):
    """ Display the user's order history. """
    
    order = get_object_or_404(Order, order_number=order_number)
    
    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))
    
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'only_message_text': True,
        'from_profile': True,
    }
    
    return render(request, template, context)

def order_management(request, order_number):
    """ Display the user's order history. """
    
    order = get_object_or_404(Order, order_number=order_number)
    
    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))
    
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'only_message_text': True,
        'management': True,
    }
    
    return render(request, template, context)

def verify_profile(request, user_id):
    """ Verify the user's profile. """
    
    profile = get_object_or_404(UserProfile, user=user_id)
    
    if profile.verified:
        messages.error(request, 'Profile already verified')
    else:
        profile.verified = True
        profile.save()
        messages.success(request, 'Profile verified successfully')
        return redirect(reverse('profile'))
    
    template = 'profiles/profile.html'
    context = {
        'profile': profile,
        'only_message_text': True,
    }
    
    return render(request, template, context)
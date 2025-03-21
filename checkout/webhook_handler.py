# Created by Matthew G Da Silva 18/13/25
# code from Code Institute Boutique Ado project
# this file is used to handle the webhooks from stripe

import json
import time
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderItem
from profiles.models import UserProfile
from products.models import Item

import stripe

class StripeWH_Handler:
    """
    Handle Stripe webhooks
    """
    
    def __init__(self, request):
        self.request = request  
    
    def _send_confirmation_email(self, order):
        """
        Send the user a confirmation email
        """        
        print('send confirmation email')
        customer_email = order.user_profile.email_address
        
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'store_contact_email': settings.DEFAULT_FROM_EMAIL, 'store_address': settings.STORE_ADDRESS, 'store_phone_number': settings.STORE_PHONE_NUMBER})
        
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )
    
    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled Webhook received: {event["type"]}',
            status=200)
        
    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        
        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        username = intent.metadata.username
        start_date = intent.metadata.start_date
        end_date = intent.metadata.end_date
        
        profile = UserProfile.objects.get(user__username=username)
        
        # get charge object
        stripe_charge = stripe.Charge.retrieve(intent.latest_charge)
        
        billing_details = stripe_charge.billing_details
        total = round(stripe_charge.amount / 100, 2)
        
        # Clean data in the billing details
        for field, value in billing_details.address.items():
            if value == "":
                billing_details.address[field] = None
        
        # check if order exists
        order_exists = False
        attempt = 1
        order = None
        while attempt <= 5:
            try:
                order = Order.objects.get(stripe_pid=pid)
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            # order was created in the view
            # send confirmation email
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    user_profile=profile,
                    start_date=start_date,
                    end_date=end_date,
                    stripe_pid=pid,
                    original_cart=cart,
                )            
                for item_id, item_data in json.loads(cart).items():
                    item = Item.objects.get(id=item_id)
                    order_line_item = OrderItem(
                            order=order,
                            item=item,
                            quantity=item_data,
                        )
                    order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        
        # order is created in webhook
                           
        # set the cart in the request session to empty
        if 'cart' and 'start_date' and 'end_date' in self.request.session:
            del self.request.session['cart']
            del self.request.session['start_date']
            del self.request.session['end_date']
        
        # send confirmation email
        self._send_confirmation_email(order)
        
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)
        
    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
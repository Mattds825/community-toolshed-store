# Created by Matthew G Da Silva 18/13/25
# code from Code Institute Boutique Ado project
# this file is used to handle the webhooks from stripe

from django.http import HttpResponse

class StripeWH_Handler:
    """
    Handle Stripe webhooks
    """
    
    def __init__(self, request):
        self.request = request  
    
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
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
        
    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
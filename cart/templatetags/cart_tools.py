from django import template


register = template.Library()

@register.simple_tag
def calc_subtotal(price, quantity, days_amount):
    return price * quantity * days_amount
from django.shortcuts import get_object_or_404
from products.models import Item

def cart_contents(request):
    
    cart_items = []
    total = 0
    product_count = 0
    start_date = None
    end_date = None
    
    cart = request.session.get('cart', {})
    
    # iterate through the cart items and get the item and quantity
    # then calculate the total and product and count and append the item to the cart_items list
    for item_id, quantity in cart.items():
        item = get_object_or_404(Item, pk=item_id)
        total += quantity * item.price
        product_count += quantity
        cart_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'item': item,
        })
        
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return context
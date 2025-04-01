from django.shortcuts import get_object_or_404
from products.models import Item, Tool
from datetime import datetime

def cart_contents(request):
    
    cart_items = []
    total = 0
    product_count = 0
    start_date = None
    end_date = None
    days_amount = 0
    
    cart = request.session.get('cart', {})
    
    start_date = request.session.get('start_date', datetime.now().strftime('%Y-%m-%d'))
    end_date = request.session.get('end_date', datetime.now().strftime('%Y-%m-%d'))
    
    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
    
    days_amount = (end_date_dt - start_date_dt).days
    
    # iterate through the cart items and get the item and quantity
    # then calculate the total (multiplied by amount of days) and product and count and append the item to the cart_items list
    for item_id, quantity in cart.items():
        
        # calculate the amount of days in the hire        
        
        item = get_object_or_404(Item, pk=item_id)
        total += (quantity * item.price) * days_amount
        product_count += quantity
        
        available_amount = None
        if item.type == 0:
            available_amount = Tool.objects.filter(sku=item.sku, is_available=True).count()
        else:
            available_amount[item_id] = item.stock_amount
        
        cart_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'item': item,
            'available_amount': available_amount,
        })
    
    if 'start_date' in request.session:
        start_date = request.session['start_date']
    if 'end_date' in request.session:
        end_date = request.session['end_date']     
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,       
        'start_date': start_date,
        'end_date': end_date, 
        'days_amount': days_amount,
    }
    
    return context
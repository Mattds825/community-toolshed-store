def cart_contents(request):
    
    cart_items = []
    total = 0
    product_count = 0
    start_date = None
    end_date = None
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return context
from django.shortcuts import render, redirect
from products.models import Item

# Create your views here.

def view_cart(request):
    """
    A view to return the cart page
    """
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """
    Add a quantity of the specified product to the shopping cart
    """
    
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    
    print("add to cart view")
    
    print(start_date, end_date)
    
    cart = request.session.get('cart', {})
    
    # cart[start_date] = start_date
    # cart[end_date] = end_date
    
    if item_id in list(cart.keys()):
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity
        
    request.session['cart'] = cart
    request.session['start_date'] = start_date
    request.session['end_date'] = end_date
    
    print(request.session['cart'])
    print(redirect_url)
    
    product = Item.objects.get(pk=item_id)
    # check if the product is a tool, if it is this means there are multiple tools with the same sku
    # so we need to redirect to the next available tool
    if product.type == 0:
        next_available_tool = Item.objects.filter(sku=product.sku, is_available=True).first()
        redirect_url = f'/products/{next_available_tool.id}'

        
    
    return redirect(redirect_url)
from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from products.models import Item, Tool, PartyItem
from profiles.models import UserProfile

# Create your views here.

def view_cart(request):
    """
    A view to return the cart page
    """
    
    profile = None
    
    if request.user.is_authenticated:
        user = request.user
        profile = UserProfile.objects.get(user=user)
        
        context = {
            'profile': profile
        }
       
    return render(request, 'cart/cart.html', context)


def add_to_cart(request, item_id):
    """
    Add a quantity of the specified product to the shopping cart
    """
    
    redirect_url = request.POST.get('redirect_url')
    
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to add items to your cart')
        return redirect(redirect_url)
    
    item = get_object_or_404(Item, pk=item_id)
    
    quantity = int(request.POST.get('quantity'))
    
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
        messages.success(request, f'Added {item.name} to your cart')
        
    request.session['cart'] = cart
    request.session['start_date'] = start_date
    request.session['end_date'] = end_date
    
    print(request.session['cart'])      
    
    product = get_object_or_404(Item,  pk=item_id)
    # check if the product is a tool, if it is this means there are multiple tools with the same sku
    # so we need to redirect to the next available tool
    if product.type == 0:
        next_available_tool = Tool.objects.filter(sku=product.sku, is_available=True).first()
        redirect_url = f'/products/{next_available_tool.id}'

        
    
    return redirect(redirect_url)


def adjust_cart(request, item_id):
    """
    Adjust the quantity of the specified product to the specified amount
    """
    quantity = int(request.POST.get('quantity'))    
    
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    
    cart = request.session.get('cart', {})
    
    item = get_object_or_404(Item, pk=item_id)
    
    # set the cart item to the new quantity
    # remove the item from the cart if the quantity is 0
    if quantity > 0:
        cart[item_id] = quantity
        messages.success(request, f'Updated {item.name} quantity to {quantity}')
    else:
        cart.pop(item_id)
        messages.success(request, f'Removed {item.name} from your cart')
    
    request.session['cart'] = cart
    
    return redirect(reverse('view_cart'))

def remove_from_cart(request, item_id):
    """
    Remove the item from the shopping cart
    return a http 200 response or 500 response
    """
    
    print("remove from cart view")
    
    try:
        cart = request.session.get('cart', {})
        cart.pop(item_id)
        
        request.session['cart'] = cart
        
        item = get_object_or_404(Item, pk=item_id)
        
        messages.success(request, f'removed {item.name} from cart')
        
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
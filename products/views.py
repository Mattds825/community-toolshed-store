from django.shortcuts import render

from .models import Item, Tool, PartyItem

# Create your views here.

def all_products(request):
    """
    A view to show all products, including sorting and search queries
    """
    
    products = Item.objects.all()
    tools = Tool.objects.all()
    party_items = PartyItem.objects.all()
    
    # for each of the products, add the image to the product depending on the type of product
    for product in products:
        if product.type == 0:            
            product.image = product.tool.image
            product.price = product.tool.price
            product.rating = product.tool.rating
        elif product.type == 1:
            product.image = product.party_item.image
            product.price = product.party_item.price
            product.rating = product.party_item.rating
    
    context = {
        'products': products,
        'tools': tools,
        'party_items': party_items,
    }
    
    return render(request, 'products/products.html', context)
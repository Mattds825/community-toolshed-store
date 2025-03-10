from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q, Case, When, CharField, ImageField
from .models import Item, Tool, PartyItem

# Create your views here.

def all_products(request):
    """
    A view to show all products, including sorting and search queries
    """
    
    products = Item.objects.all()
    
    query = None
    
    # for each of the products, add the image to the product depending on the type of product        
    products = Item.objects.all().annotate(
        description=Case(
            When(type=0, then='tool__description'),
            When(type=1, then='partyitem__description'),
            output_field=CharField(),
        ),
        keywords=Case(
            When(type=0, then='tool__keywords'),
            When(type=1, then='partyitem__keywords'),
            output_field=CharField(),
        ),       
        price=Case(
            When(type=0, then='tool__price'),
            When(type=1, then='partyitem__price'),
            output_field=CharField(),
        ),
        rating=Case(
            When(type=0, then='tool__rating'),
            When(type=1, then='partyitem__rating'),
            output_field=CharField(),
        )
    )
    
    # quick fix to add image to product
    for product in products:
        if product.type == 0:            
            product.image = product.tool.image
        elif product.type == 1:
            product.image = product.party_item.image
    
    
    # handle request to filter products by category
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products')) 
            
            queries = Q(name__icontains=query) | Q(description__icontains=query) | Q(keywords__icontains=query)
            products = products.filter(queries)
            
            # quick fix to add image to product
            for product in products:
                if product.type == 0:            
                    product.image = product.tool.image
                elif product.type == 1:
                    product.image = product.party_item.image
        
    
    context = {
        'products': products, 
        'search_term': query,
    }
    
    return render(request, 'products/products.html', context)

def product_detail(request, product_id): 
    """
    A view to show individual product details
    """
    
    product = get_object_or_404(Item, pk=product_id)
    
    if product.type == 0:
        product.image = product.tool.image
        product.price = product.tool.price
        product.rating = product.tool.rating
        product.description = product.tool.description
    elif product.type == 1:
        product.image = product.party_item.image
        product.price = product.party_item.price
        product.rating = product.party_item.rating
        product.description = product.party_item.description
    
    context = {
        'product': product,
    }
    
    return render(request, 'products/product_detail.html', context)
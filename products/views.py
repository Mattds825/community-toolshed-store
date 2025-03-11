from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q, F, Case, When, CharField, ImageField, IntegerField
from django.db.models.functions import Lower
from .models import Item, Tool, PartyItem, Category

# Create your views here.

def all_products(request):
    """
    A view to show all products, including sorting and search queries
    """
    
    products = Item.objects.all()
    
    query = None
    categories = None
    sort = None
    direction = None
    
    
    
    # handle request to filter products by category
    if request.GET:
        # check sort and direction parameter
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey == 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey) 
                
        # check category parameter
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')            
            products = products.filter(category__name__in=categories)                                                
            categories = Category.objects.filter(name__in=categories)            
        # check q parameter
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products')) 
            
            queries = Q(name__icontains=query) | Q(description__icontains=query) | Q(keywords__icontains=query)
            products = products.filter(queries)
                   
        
    current_sorting = f'{sort}_{direction}' 
    
    context = {
        'products': products, 
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }
    
    return render(request, 'products/products.html', context)

def product_detail(request, product_id): 
    """
    A view to show individual product details
    """
    
    product = get_object_or_404(Item, pk=product_id)  
    
    context = {
        'product': product,
    }
    
    return render(request, 'products/product_detail.html', context)
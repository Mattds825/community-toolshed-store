from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q, F, Case, When, CharField, ImageField, IntegerField
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
    
    # for each of the products, add the image to the product depending on the type of product        
    products = Item.objects.all().annotate(
        description=Case(
            When(type=0, then=F('tool__description')),
            When(type=1, then=F('partyitem__description')),
            output_field=CharField(),
        ),
        keywords=Case(
            When(type=0, then=F('tool__keywords')),
            When(type=1, then=F('partyitem__keywords')),
            output_field=CharField(),
        ),
        image=Case(
            When(type=0, then=F('tool__image')),
            When(type=1, then=F('partyitem__image')),
            output_field=ImageField(),
        ),
        price=Case(
            When(type=0, then=F('tool__price')),
            When(type=1, then=F('partyitem__price')),
            output_field=CharField(),
        ),
        rating=Case(
            When(type=0, then=F('tool__rating')),
            When(type=1, then=F('partyitem__rating')),
            output_field=CharField(),
        ),
        category=Case(
            When(type=0, then=F('tool__category__name')),
            When(type=1, then=F('partyitem__category__name')),
            output_field=CharField(),
        ),
    )
    
    # quick fix to add image to product
    for product in products:        
        if product.type == 0:            
            product.image = product.tool.image            
        elif product.type == 1:
            product.image = product.party_item.image            
    
    
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
            products = products.filter(category__in=categories)                                                
            categories = Category.objects.filter(name__in=categories)            
        # check q parameter
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
    
    if product.type == 0:
        product.image = product.tool.image
        product.price = product.tool.price
        product.rating = product.tool.rating
        product.description = product.tool.description
        product.category = product.tool.category
    elif product.type == 1:
        product.image = product.party_item.image
        product.price = product.party_item.price
        product.rating = product.party_item.rating
        product.description = product.party_item.description
        product.category = product.party_item.category
    
    context = {
        'product': product,
    }
    
    return render(request, 'products/product_detail.html', context)
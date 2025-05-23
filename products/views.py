from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q, F, Case, When, CharField, ImageField, IntegerField, Count
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required

from .models import Item, Tool, PartyItem, Category
from checkout.models import Order
from .forms import ToolForm, PartyItemForm

# Create your views here.

def all_products(request):
    """
    A view to show all products, including sorting and search queries
    """

    products = Item.objects.all()
    
    # items should be filtered to only have one of of each sku
    # this is because we can have multiple tools
    # products = products.distinct('sku')
    
    query = None
    categories = None
    sort = None
    direction = None
    
    sortkey = None
    
    
    # remove sku duplicates
    filteredProducts = Item.objects.none()
    sku_list = []
    
    
    for product in products:        
        if product.type == 0:
            if product.sku not in sku_list:
                sku_list.append(product.sku)
                filteredProducts |= Item.objects.filter(id=product.id)
        else:
            sku_list.append(product.sku)
            filteredProducts |= Item.objects.filter(id=product.id)
            
    products = filteredProducts                         
    
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
                          
    
    #  # Apply distinct on SKU
    # if sort:
    #     products = products.order_by('sku', sortkey)
    # else:
    #     products = products.order_by('sku')
    # products = products.distinct('sku')
    
    # remove all products that have duplicate skus and are of type tool
    # products = products.filter(type=1).distinct('sku')
    
    # Annotate the queryset with a unique identifier for each SKU
        
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
    
    # get amount of items with same sku
    
    product = get_object_or_404(Item, pk=product_id)  
    
    available_amount = None
    cart_amount = None
    
    # check if the product is a tool
    # if it is a tool, get the amount of available tools
    # if it is a party item, get the stock amount
    if product.type == 0:
        available_amount = Tool.objects.filter(sku=product.sku, is_available=True).count()
    else:
        party_item = PartyItem.objects.get(id=product_id)   
        available_amount = party_item.stock_amount
        
    cart = request.session.get('cart', {})
    
    if cart:
        if product_id in cart:            
            cart_amount = cart[product_id]
            available_amount = available_amount - cart_amount    
        
    
    context = {
        'product': product,
        'available_amount': available_amount,
        'cart_amount': cart_amount,
    }
    
    return render(request, 'products/product_detail.html', context)

@login_required
def management(request):
    """
    A view to show the management page
    """
    
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can access this page.')
        return redirect(reverse('homepage'))
    
    items = Item.objects.all()
    tools = Tool.objects.all()
    party_items = PartyItem.objects.all()
    orders = Order.objects.all()
    
    context = {
        'tools': tools,
        'party_items': party_items,
        'orders': orders,
        'items': items,
    }
    
    return render(request, 'products/management.html', context)

@login_required
def add_tool(request):
    """
    Add a Tool to the store
    """
    
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can access this page.')
        return redirect(reverse('homepage'))
    
    if request.method == 'POST':
        form = ToolForm(request.POST, request.FILES)
        if form.is_valid():
            tool = form.save()
            messages.success(request, 'Successfully added tool!')
            return redirect(reverse('product_detail', args=[tool.id]))
        else:
            messages.error(request, 'Failed to add tool. Please ensure the form is valid.')
    else:
        form = ToolForm()    
    
    context = {
        'form': form,
        'type': 'tool',
    }
    
    template = 'products/add_product.html'
    
    return render(request, template, context)    

@login_required
def add_party_item(request):
    """
    Add a Party Item to the store
    """
    
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can access this page.')
        return redirect(reverse('homepage'))
    
    if request.method == 'POST':
        form = PartyItemForm(request.POST, request.FILES)
        if form.is_valid():
            party_item = form.save()
            messages.success(request, 'Successfully added party item!')
            return redirect(reverse('product_detail', args=[party_item.id]))
        else:
            messages.error(request, 'Failed to add party item. Please ensure the form is valid.')
    else:
        form = PartyItemForm()    
    
    context = {
        'form': form,  
        'type': 'party_item',     
    }
    
    template = 'products/add_product.html'
    
    return render(request, template, context)
    
    
@login_required
def edit_tool(request, item_id):
    """
    Edit a Tool in the store
    """
    
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can access this page.')
        return redirect(reverse('homepage'))
    
    tool = get_object_or_404(Tool, pk=item_id)
    
    if request.method == 'POST':
        form = ToolForm(request.POST, request.FILES, instance=tool)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated tool!')
            return redirect(reverse('product_detail', args=[tool.id]))
        else:
            messages.error(request, 'Failed to update tool. Please ensure the form is valid.')
    else:
        form = ToolForm(instance=tool)
    
    context = {
        'form': form,
        'tool': tool,
        'type': 'tool',
    }
    
    return render(request, 'products/edit_product.html', context)

@login_required
def edit_party_item(request, item_id):
    """
    Edit a Party Item in the store
    """
    
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can access this page.')
        return redirect(reverse('homepage'))
    
    party_item = get_object_or_404(PartyItem, pk=item_id)
    
    if request.method == 'POST':
        form = PartyItemForm(request.POST, request.FILES, instance=party_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated party item!')
            return redirect(reverse('product_detail', args=[party_item.id]))
        else:
            messages.error(request, 'Failed to update party item. Please ensure the form is valid.')
    else:
        form = PartyItemForm(instance=party_item)
    
    context = {
        'form': form,
        'party_item': party_item,
        'type': 'party_item',
    }
    
    return render(request, 'products/edit_product.html', context)

@login_required
def delete_item(request, item_id):
    "delete an item from the store"
    
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can access this page.')
        return redirect(reverse('homepage'))
    
    item = get_object_or_404(Item, pk=item_id)
    item.delete()
    messages.success(request, 'Item deleted!')
    return redirect(reverse('management'))
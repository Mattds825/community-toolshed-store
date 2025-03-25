from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import MaintenanceTicket
from products.models import Tool
from checkout.models import Order
from .forms import MaintenanceTicketForm

# Create your views here.

def maintenance(request):
    """ A view to return the maintenance page """
    
    tickets = MaintenanceTicket.objects.all()
    
    active_tickets = tickets.filter(status='pending')
    
    other_tickets = tickets.exclude(status='pending')
    
    context = {
        'tickets': tickets,
        'active_tickets': active_tickets,
        'other_tickets': other_tickets
    }
    

    return render(request, 'maintenance/maintenance.html', context)

def create_ticket(request, tool_id, order_id):
    """ 
    A view to return the create ticket page 
    from a specific tool
    """
    
    tool = Tool.objects.get(pk=tool_id)
    order = Order.objects.get(pk=order_id)
    
    if request.method == 'POST':
        form = MaintenanceTicketForm(request.POST)
                
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully create a maintenance ticket!')
            return redirect(reverse('maintenance'))
        else:
            messages.error(request, 'Failed to create the ticket. Please ensure the form is valid.')
    else:
        form = MaintenanceTicketForm(
            initial={
                'tool': tool,
                'associated_order': order,
            }
        )
    
    context = {
        'tool': tool,
        'form': form
    }
    
    return render(request, 'maintenance/create_ticket.html', context)

def create_new_ticket(request):
    """ 
    A view to create a new maintenance ticket
    """
    
    if request.method == 'POST':
        form = MaintenanceTicketForm(request.POST)        
        
        print(form.fields)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully create a maintenance ticket!')
            return redirect(reverse('maintenance'))
        else:
            print('error', form.errors)
            messages.error(request, 'Failed to create the ticket. Please ensure the form is valid.')
    else:
        form = MaintenanceTicketForm()
    
    context = {
        'form': form
    }
    
    return render(request, 'maintenance/create_ticket.html', context)
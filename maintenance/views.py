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
        'form': form,
        'only_message_text': True
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
            # set the tool to inactive
            tool = Tool.objects.get(pk=form.cleaned_data['tool'].id)
            tool.is_available = False
            tool.save()
            
            form.save()
            messages.success(request, 'Successfully create a maintenance ticket!')
            return redirect(reverse('maintenance'))
        else:
            print('error', form.errors)
            messages.error(request, 'Failed to create the ticket. Please ensure the form is valid.')
    else:
        form = MaintenanceTicketForm()
    
    context = {
        'form': form,
        'only_message_text': True
    }
    
    return render(request, 'maintenance/create_ticket.html', context)

def edit_ticket(request, ticket_id):
    """ 
    A view to edit a maintenance ticket
    """
    
    ticket = MaintenanceTicket.objects.get(pk=ticket_id)
    
    # logic to ensure tickets with no associated order can be edited
    isNone = False    
    if ticket.associated_order is None:
        isNone = True
    
    if request.method == 'POST':
        form = MaintenanceTicketForm(request.POST, instance=ticket)                
        
        # print choices for associated_order
        print("choices:",form.fields['associated_order'].choices[0])
        
        # print the value of associated_order
        print('val',form['associated_order'].value())
        
            
        if form.is_valid():            
            form.save()
            messages.success(request, 'Successfully updated the maintenance ticket!')
            return redirect(reverse('maintenance'))
        else:
            print('error', form.errors)
            messages.error(request, 'Failed to update the ticket. Please ensure the form is valid.')
    else:
        form = MaintenanceTicketForm(instance=ticket)
    
    context = {
        'ticket': ticket,
        'form': form,
        'isNone': isNone,
        'only_message_text': True
    }
    
    return render(request, 'maintenance/edit_ticket.html', context)

def complete_ticket(request, ticket_id):
    """ 
    A view to complete a maintenance ticket
    """
    
    ticket = MaintenanceTicket.objects.get(pk=ticket_id)
    
     # logic to ensure tickets with no associated order can be edited
    isNone = False    
    if ticket.associated_order is None:
        isNone = True    
    
    if request.method == 'POST':
        form = MaintenanceTicketForm(request.POST, instance=ticket)
        
        if form.is_valid():
            # if the status is set to written off, set the tool to inactive
            if form['status'].value() == 'written_off':
                tool = Tool.objects.get(pk=ticket.tool.id)
                tool.is_available = False
                tool.save()
            elif form['status'].value() == 'fixed':
                tool = Tool.objects.get(pk=ticket.tool.id)
                tool.is_available = True
                tool.save()                                
            form.save()
            messages.success(request, 'Successfully completed the maintenance ticket!')
            return redirect(reverse('maintenance'))
        else:
            # print the errors
            print('error', form.errors)
            messages.error(request, 'Failed to update the ticket. Please ensure the form is valid.')
    else:
        form = MaintenanceTicketForm(instance=ticket)
    
    context = {
        'ticket': ticket,
        'form': form,
        'isNone': isNone,
        'only_message_text': True
    }
    
    return render(request, 'maintenance/complete_ticket.html', context)

def view_ticket(request, ticket_id):
    """
    A view to view a maintenance ticket
    """
    
    ticket = MaintenanceTicket.objects.get(pk=ticket_id)
    
    context = {
        'ticket': ticket
    }
    
    return render(request, 'maintenance/view_ticket.html', context)

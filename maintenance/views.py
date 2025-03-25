from django.shortcuts import render
from .models import MaintenanceTicket

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
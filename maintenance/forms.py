from django import forms
from .models import MaintenanceTicket
from products.models import Tool

class MaintenanceTicketForm(forms.ModelForm):
    """"
    Form for creating a new maintenance ticket
    """
    
    class Meta:
        model = MaintenanceTicket
        exclude = ('ticket_number',)
        
    def __init__(self, *args, **kwargs):
        super(MaintenanceTicketForm, self).__init__(*args, **kwargs)
        
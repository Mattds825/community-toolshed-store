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
        
        # add None and a blank option to the associated_order field
        self.fields['associated_order'].required = False  # Allow None as a valid value
        self.fields['associated_order'].choices = [(None, 'No Order')] + list(self.fields['associated_order'].choices)[1:]
        
from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Item, Category, Tool, PartyItem
from .widgets import CustomClearableFileInput

class ToolForm(forms.ModelForm):
    """
    Form for adding a new tool
    """
    class Meta:
        model = Tool
        exclude = ('type','rating','is_written_off','needs_repair',)
        widgets = {
            'description': SummernoteWidget(),  # Use SummernoteWidget for rich text
            'image': CustomClearableFileInput(), # Use CustomClearableFileInput for image
        }
        
    def __init__(self, *args, **kwargs):
        super(ToolForm, self).__init__(*args, **kwargs)
        
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        
        self.fields['category'].choices = friendly_names
        
        # for field_name in self.fields.items():
        #     field_name.field.widget.attrs['class'] = 'border-black rounded-0'

class PartyItemForm(forms.ModelForm):
    """
    Form for adding a new party item
    """
    class Meta:
        model = PartyItem
        exclude = ('type','rating','broken_amount',)
        widgets = {
            'description': SummernoteWidget(),  # Use SummernoteWidget for rich text
            'image': CustomClearableFileInput(), # Use CustomClearableFileInput for image
        }
        
    def __init__(self, *args, **kwargs):
        super(PartyItemForm, self).__init__(*args, **kwargs)
        
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        
        self.fields['category'].choices = friendly_names
        
        # for field_name in self.fields.items():
        #     field_name.field.widget.attrs['class'] = 'border-black rounded-0'
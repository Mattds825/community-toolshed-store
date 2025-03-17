from django import forms
from profiles.models import UserProfile
from django_countries.widgets import CountrySelectWidget

class PaymentForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        widgets = {
            'country': CountrySelectWidget(layout='{widget}', attrs={'class': 'border-black rounded-0 profile-form-input'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'email_address': 'Email Address',
            'full_name': 'Full Name',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }
        
        for field in self.fields:
            # set field to readonly
            self.fields[field].widget.attrs['readonly'] = True                
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            else:
                # set country field to disabled
                self.fields[field].widget.attrs['disabled'] = True
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            self.fields[field].label = False

from django import forms
from .models import UserProfile
from django_countries.widgets import CountrySelectWidget

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user','email_address', 'verified')
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
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'border-black profile-form-input'
            self.fields[field].label = False

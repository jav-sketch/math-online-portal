from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('Stripe', 'Stripe'),
    ('Paypal', 'Paypal'),
    ('MMG', 'MMG'),
)
class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '123 Main st'
    }))

    address_2 = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or Suite'
    }))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100'
    }))
    zip = forms.CharField()
    same_billing_address = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    save_info = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    payment = forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENT_CHOICES)

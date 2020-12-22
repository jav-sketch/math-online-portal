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
    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment = forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENT_CHOICES, required=False)


# Coupon 
class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo Code',
        'aria-label:': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2',
    }))

class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.Textarea()
    email = forms.EmailField()


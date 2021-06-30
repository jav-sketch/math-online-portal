from django.db.models import fields
from .models import UserProfile
from django import forms
from django.contrib import messages
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User


PAYMENT_CHOICES = (
    ('Stripe', 'Stripe'),
    ('Paypal', 'Paypal'),
    ('MMG', 'MMG'),
)
class CheckoutForm(forms.Form):
    # address = forms.CharField(widget=forms.TextInput(attrs={
    #     'placeholder': '123 Main st'
    # }))

    # address_2 = forms.CharField(widget=forms.TextInput(attrs={
    #     'placeholder': 'Apartment or Suite'
    # }))

    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(required=False, widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100'
    }))
    shipping_zip = forms.CharField(required=False)
    
    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(required=False, widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100'
    }))
    billing_zip = forms.CharField(required=False)


    same_billing_address = forms.BooleanField(required=False)
    # set_default_shipping = forms.BooleanField(required=False)
    # use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)
    
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
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 5
    }))
    email = forms.EmailField()

class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)    
    save = forms.BooleanField(required=False)    
    use_default = forms.BooleanField(required=False)

# Contact Form 
class ContactForm(forms.Form):
    name = forms.CharField(label='name', max_length=50)
    email  = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'row': 5
    }))

# creates user form
class UserProfileCreationform(UserCreationForm):
    unsername = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(required=True, label="First Name")
    last_name =forms.CharField(required=True, label="Last Name")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


# class UserUpdateForm(forms.ModelForm): 
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email']
       


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user','username', 'first_name', 'last_name', 'email', 'image']
        exclude = ('stripe_customer_id', 'is_staff', 'is_superuser')
        

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import fields
from django.db.models.enums import Choices
from django_countries.fields import CountryField

class CreateForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2','first_name','last_name']

decide=(
    ('card','Card Method'),
    ('cash','Cash On Delivery'),
  
)
class checkoutform(forms.Form):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First_Name'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last_Name'}))
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email=forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Type your email'}))      #pip install django-countries
    address=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Address Bar'}))
    country = CountryField(blank_label='(select country)').formfield(attrs={'class':'custom-select d-block w-100'})
    state=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type your state'}))
    zip=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Type your pincode'}))
    save_billing_add=forms.BooleanField(required=False)
    save_info=forms.BooleanField(required=False)
    payement=forms.ChoiceField(widget=forms.RadioSelect, choices=decide)

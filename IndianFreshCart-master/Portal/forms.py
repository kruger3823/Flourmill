from django import forms
from .models import Profile,Product,Order
from django import forms
from . import models
from django.contrib.auth.models import User


class Profileform(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name','last_name','gender','date_of_birth','city','state','country']
        exclude=['user']

class Productform(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ['user']

class Orderform(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
        exclude=['user']


class StaffUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
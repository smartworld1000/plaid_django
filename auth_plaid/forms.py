from django import forms
from django.forms import ModelForm
from .models import UserSignupPlus

class UserSignupForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32
    )
    email = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 32,
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):        
        kwargs.setdefault('label_suffix', '')
        super(UserSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = "Username*"
        self.fields['email'].widget.attrs['placeholder'] = 'Email address'
        self.fields['email'].label = "Email address*"
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        self.fields['password'].label = "Password*"

class UserSignupPlusForm(ModelForm):
    class Meta:
        model = UserSignupPlus
        fields = ['email_address', 'city', 'state', 'zip_code', 'country', 'home_phone', 'birth_date', 'gender']

    def __init__(self, *args, **kwargs):        
        kwargs.setdefault('label_suffix', '')
        super(UserSignupPlusForm, self).__init__(*args, **kwargs)
        self.fields['email_address'].widget.attrs['placeholder'] = 'Email address'
        self.fields['email_address'].label = "Email address(again please)*"
        self.fields['city'].widget.attrs['placeholder'] = 'City'
        self.fields['city'].label = "City*"
        self.fields['state'].widget.attrs['placeholder'] = 'State'
        self.fields['state'].label = "State*"
        self.fields['zip_code'].widget.attrs['placeholder'] = 'Zip code'
        self.fields['zip_code'].label = "Zip code*"
        self.fields['country'].widget.attrs['placeholder'] = 'Country'
        self.fields['country'].label = "Country*"
        self.fields['home_phone'].widget.attrs['placeholder'] = 'Phone number'
        self.fields['home_phone'].label = "Home Phone number*"
        self.fields['birth_date'].widget.attrs['placeholder'] = 'Birth date(e.g: 2000-01-01)'
        self.fields['birth_date'].label = "Birth date*"
        self.fields['gender'].widget.attrs['placeholder'] = 'Gender'
        self.fields['gender'].label = "Gender*"
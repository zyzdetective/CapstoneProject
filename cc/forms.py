from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


# class SignupForm(UserCreationForm):
#     # username = forms.CharField(label='Your username')
#     # email = forms.EmailField(label='Your email')
#     # password = forms.CharField(label='Your password')
#     # user_type = forms.ModelForm(forms.User)
#     pass

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'user_type']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
        }


class SponsorProfileForm(forms.Form):
    sponsor_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sponsor_description = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    what_we_have = forms.ChoiceField(required=True, choices=((1, 'Food'), (2, 'Cloth'), (3, 'Accommodation')),
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    website = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))


class CharityProfileForm(forms.Form):
    charity_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    charity_description = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    what_we_need = forms.ChoiceField(required=True, choices=((1, 'Food'), (2, 'Cloth'), (3, 'Accommodation')),
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    other_needs = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    website = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))


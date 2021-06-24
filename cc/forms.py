from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserCharity, UserSponsor


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


class LoginForm(forms.Form):
    username = forms.CharField(label='Your username')
    password = forms.CharField(label='Your password')


class EditForm(forms.ModelForm):
    class Meta:
        model = UserCharity
        fields = ['long_name', 'description', 'website']



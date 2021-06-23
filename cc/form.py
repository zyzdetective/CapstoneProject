from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(label='Your username')
    email = forms.EmailField(label='Your email')
    password = forms.CharField(label='Your password')



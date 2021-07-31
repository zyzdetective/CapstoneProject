from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserCharity, UserSponsor


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type']


class SigninForm(forms.Form):
    username = forms.CharField(label='Your username')
    password = forms.CharField(widget=forms.PasswordInput, label='Your password')


class EditForm(forms.ModelForm):
    class Meta:
        model = UserCharity
        fields = ['long_name', 'description', 'website']
        widgets = {'description': forms.Textarea(attrs={'class': 'description_css'}),
                   }


class ItemForm(forms.Form):
    items = forms.MultipleChoiceField(
        choices=(('Food', 'Food'), ('Cloth', 'Cloth'), ('Accommodation', 'Accommodation')),
        widget=forms.CheckboxSelectMultiple(), )
    # personal need or provide
    other_items = forms.CharField(widget=forms.TextInput(), required=False)


class PageForm(forms.Form):
    page = forms.IntegerField(widget=forms.NumberInput(), initial=1)


class ConnectForm(forms.Form):
    message = forms.Field(widget=forms.Textarea(), required=False)


class MessageForm(forms.Form):
    message_reply = forms.Field(widget=forms.Textarea(), required=True)
    your_reply = forms.ChoiceField(choices=(('2', 'Accept'), ('3', 'Reject')), widget=forms.Select())


class RecommendationForm(forms.Form):
    recommendation_choice = forms.ChoiceField(
        choices=((0, 'All Sponsors'), (1, 'At least One Connection Sponsors'), (2, 'Zero Connection Sponsors')),
        widget=forms.Select())


class SearchForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(), required=False, label='Name')
    description = forms.CharField(widget=forms.TextInput(), required=False, label='description')
    need = forms.CharField(widget=forms.TextInput(), required=False, label='Need')

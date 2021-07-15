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


class SigninForm(forms.Form):
    username = forms.CharField(label='Your username')
    password = forms.CharField(label='Your password')


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

    other_items = forms.CharField(widget=forms.TextInput(), required=False)


class PageForm(forms.Form):
    page = forms.IntegerField(widget=forms.NumberInput(), initial=1)


class ConnectForm(forms.Form):
    message = forms.Field(widget=forms.Textarea(), required=False)


class MessageForm(forms.Form):
    message_reply = forms.Field(widget=forms.Textarea(), required=True)
    your_reply = forms.ChoiceField(choices=(('2', 'Agree'), ('3', 'Disagree')), widget=forms.Select())


class RecommendationForm(forms.Form):
    recommendation_choice = forms.ChoiceField(choices=((0, 'All Sponsors'), (1, 'At least one connection Sponsors'), (2, 'Zero connection Sponsors')), widget=forms.Select())

# class CharityProfileForm(forms.Form):
#     charity_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     charity_description = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     what_we_need = forms.ChoiceField(required=True, choices=((1, 'Food'), (2, 'Cloth'), (3, 'Accommodation')),
#                                      widget=forms.Select(attrs={'class': 'form-control'}))
#     other_needs = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     website = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

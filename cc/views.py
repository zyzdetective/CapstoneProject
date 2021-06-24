from django.shortcuts import render
from cc.forms import SignupForm, LoginForm, SponsorProfileForm, CharityProfileForm
from cc.models import User, UserCharity, UserSponsor


# Create your views here.

def signup(request):
    if request.method == 'GET':

        signup_form = SignupForm
    else:
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            username = signup_form.data.get('username')
            email = signup_form.data.get('email')
            password = signup_form.data.get('password')
            user_type = signup_form.data.get('user_type')
            print(username, email, password, user_type)

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                user_type=user_type,
            )
            charity = UserCharity.objects.create(user=user, long_name='frank')

    # except Exception as e:
    # return print('fail')

    return render(request=request,
                  template_name="cc/signup.html",
                  context={"form": signup_form})

def login(request):
    if request.method == 'GET':
        login_form = LoginForm

    else:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.data.get('username')
            password = login_form.data.get('password')
            user_type = login_form.data.get('user_type')
            print(username, password, user_type)
    return render(request=request,
                  template_name="cc/login.html",
                  context={"form": login_form}
                  )


def home(request):
    return render(request=request,
                  template_name="cc/home.html",
                  )

def sponsor_profile(request):
    if request.method == 'GET':
        sponsor_profile_form = SponsorProfileForm
    else:
        sponsor_profile_form = SponsorProfileForm(request.POST)
        if sponsor_profile_form.is_valid():
            sponsor_name = sponsor_profile_form.data.get('sponsor_name')
            sponsor_description = sponsor_profile_form.data.get('sponsor_description')
            sponsor_needs = sponsor_profile_form.data.get('what_we_have')
            website = sponsor_profile_form.data.get('website')
            print(sponsor_name, sponsor_description, sponsor_needs, website)
    return render(request=request,
                  template_name="cc/S_profile.html",
                  context={"form": sponsor_profile_form}
                  )


def charity_profile(request):
    if request.method == 'GET':
        charity_profile_form = CharityProfileForm
    else:
        charity_profile_form = CharityProfileForm(request.POST)
        if charity_profile_form.is_valid():
            charity_name = charity_profile_form.data.get('charity_name')
            charity_description = charity_profile_form.data.get('charity_description')
            charity_needs = charity_profile_form.data.get('what_we_need')
            other_needs = charity_profile_form.data.get('other_needs')
            website = charity_profile_form.data.get('website')
            print(charity_name, charity_description, charity_needs, other_needs, website)
    return render(request=request,
                  template_name="cc/C_profile.html",
                  context={"form": charity_profile_form}
                  )
from django.shortcuts import render, redirect, HttpResponse
from cc.forms import SignupForm, LoginForm, EditForm
from cc.models import User, UserCharity, UserSponsor, Need, Provide
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required

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

    return render(request=request,
                  template_name="cc/test_sign.html",
                  context={"form": signup_form})


def signin(request):
    if request.method == 'GET':

        signin_form = LoginForm
    else:
        signin_form = LoginForm(request.POST)
        username = signin_form.data.get('username')
        password = signin_form.data.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print('successful')
            login(request, user)
            # Redirect to a success page.
            return redirect("/edit/")
        else:
            # Return an 'invalid login' error message.
            print('unsuccessful')
            return render(request=request,
                          template_name="cc/test_signin.html",
                          context={"form": signin_form,
                                   "error": "invalid username or password"})

    return render(request=request,
                  template_name="cc/test_signin.html",
                  context={"form": signin_form})



def edit(request):
    if request.method == 'GET':

        edit_form = EditForm
    else:
        user = request.user
        print(f'user:{user}')
        edit_form = EditForm(request.POST)
        long_name = edit_form.data.get('long_name')
        description = edit_form.data.get('description')
        website = edit_form.data.get('website')
        print(long_name, description, website)
        items=['1','2','3']
        # charity = UserCharity.objects.update(user=user, long_name='frank')





    return render(request=request,
                  template_name="cc/test_signin.html",
                  context={"form": edit_form})



def logout(request):
    ppp = logout(request)
    print(f'logout {ppp}') # None
    return redirect("/signin/")


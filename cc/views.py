from django.shortcuts import render
from cc.forms import SignupForm
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
                  template_name="cc/test_sign.html",
                  context={"form": signup_form})

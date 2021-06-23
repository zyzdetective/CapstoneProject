from django.shortcuts import render
from cc.form import SignupForm
from cc.models import User,User_Type_1,User_Type_2
# Create your views here.

def signup(request):
    if request.method == 'GET':

        signup_form = SignupForm
    else:
        signup_form = SignupForm(request.POST)

    username = '2'
    email = '1@q.com'
    password = '1'

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )
    usertype_1 = User_Type_1.objects.create(user=user, user_type_1_teyoushuxing='frank')

    #except Exception as e:
        #return print('注册失败')

    return render(request = request,
                  template_name = "cc/test_sign.html",
                  context={"form":signup_form})
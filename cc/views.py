from django.shortcuts import render
from cc.form import SignupForm

# Create your views here.

def signup(request):
    if request.method == 'GET':

        signup_form = SignupForm
    else:
        signup_form = SignupForm(request.POST)
        


    return render(request = request,
                  template_name = "cc/test_sign.html",
                  context={"form":signup_form})
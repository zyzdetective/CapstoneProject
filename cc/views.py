from django.shortcuts import render, redirect, HttpResponse
from cc.forms import SignupForm, SigninForm, EditForm
from cc.models import User, UserCharity, UserSponsor, Need, Provide
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required


# Create your views here.


def signup(request):
    print(f'current user:{request.user}')
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
            if int(user_type[0]) == 1:
                charity = UserCharity.objects.create(user=user,username=username,email=email)
            else:
                sponsor = UserSponsor.objects.create(user=user,username=username,email=email)

    return render(request=request,
                  template_name="cc/test_sign.html",
                  context={"form": signup_form})


def signin(request):
    print(f'current user:{request.user}')
    if request.method == 'GET':

        signin_form = SigninForm
    else:
        signin_form = SigninForm(request.POST)
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


@login_required()
def edit(request):
    print(f'current user:{request.user}')
    if request.method == 'GET':

        edit_form = EditForm
    else:
        user = request.user  #this user -> User.username
        user_type = request.user.user_type
        print(f'user:{user}')
        edit_form = EditForm(request.POST)
        long_name = edit_form.data.get('long_name')
        description = edit_form.data.get('description')
        website = edit_form.data.get('website')
        print(long_name, description, website)
        items = ['5', '6', '7']

        if user_type == 1:  #update table Charity and need
            update_obj = UserCharity.objects.get(username=user)
            update_item = Need
        else:   #update table Sponsor and provide
            update_obj = UserSponsor.objects.get(username=user)
            update_item = Provide

        update_obj.long_name = long_name
        update_obj.description = description
        update_obj.website = website
        update_obj.save()

        # update table Need or provide
        current_need_list = []
        # items means the newest updated need list
        # current_need means each need in current databases
        for current_need in list(update_item.objects.filter(username_id__exact=user).values_list('need')):
            current_need = current_need[0]
            current_need_list.append(current_need)
            # delete old need ( not in newest )
            if current_need not in items:
                update_item.objects.get(username_id=user, need=current_need).delete()

        for item in items:
            # create new need ( not in current_need )
            if item not in current_need_list:
                update_item.objects.create(username=user, need=item)

        # finishing update table Need or provide

    return render(request=request,
                  template_name="cc/test_signin.html",
                  context={"form": edit_form})


@login_required
def signout(request):
    print(f'current user:{request.user}')
    out = logout(request)
    print(f'signout {out}')  # None
    return redirect("/signin/")

from django.shortcuts import render, redirect, HttpResponse
from cc.forms import SignupForm, SigninForm, EditForm, ItemForm, PageForm, ConnectForm, MessageForm
from cc.models import User, UserCharity, UserSponsor, Need, Provide, Message, Connect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Count
import math
from django import forms


# Create your views here.

def base(request):
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    return render(request=request,
                  template_name="base/base.html",
                  context={'signin_status': signin_status,
                           'current_user': request.user, }
                  )


def signup(request):
    print(f'current user:{request.user}')
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
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
                charity = UserCharity.objects.create(user=user, username=username, email=email)
            else:
                sponsor = UserSponsor.objects.create(user=user, username=username, email=email)
            return redirect("/home/")
    return render(request=request,
                  template_name="cc/signup.html",
                  context={"form": signup_form,
                           'signin_status': signin_status,
                           'current_user': request.user,
                           })


def signin(request):
    print(f'current user:{request.user}')
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
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
            return redirect("/home/")
        else:
            # Return an 'invalid login' error message.
            print('unsuccessful')
            return render(request=request,
                          template_name="cc/signin.html",
                          context={"form": signin_form,
                                   "error": "invalid username or password",
                                   'signin_status': signin_status,
                                   'current_user': request.user,
                                   })

    return render(request=request,
                  template_name="cc/signin.html",
                  context={"form": signin_form,
                           'signin_status': signin_status,
                           'current_user': request.user,
                           })


@login_required
def edit(request):
    print(f'current user:{request.user}')
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    if request.method == 'GET':

        edit_form = EditForm
        item_form = ItemForm
    else:
        user = request.user  # this user -> User.username
        user_type = request.user.user_type
        print(f'user:{user}')
        edit_form = EditForm(request.POST)
        item_form = ItemForm(request.POST)
        long_name = edit_form.data.get('long_name')
        description = edit_form.data.get('description')
        website = edit_form.data.get('website')
        items = item_form.data.getlist('items')
        other_items = item_form.data.get('other_items')
        if other_items:
            for ele in other_items.split(','):
                items.append(ele.strip())
        print(long_name, description, website, items, other_items)

        if user_type == 1:  # update table Charity and need
            update_obj = UserCharity.objects.get(username=user)
            update_item = Need
        else:  # update table Sponsor and provide
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
        return redirect(f'/details/{user}')

    return render(request=request,
                  template_name="cc/add_profile.html",
                  context={"edit_form": edit_form,
                           "user_type": request.user.user_type,
                           "item_form": item_form,
                           'signin_status': signin_status,
                           'current_user': request.user,
                           })


@login_required
def signout(request):
    print(f'current user:{request.user}')

    out = logout(request)
    print(f'signout {out}')  # None
    return redirect("/signin/")


def details(request, details_slug):
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    try:
        user = User.objects.get(username=details_slug)
        if request.method == 'GET':
            username = user.username
            user_type = user.user_type
            connection_list = []
            if user_type == 1:  # update table Charity and need
                user_profile = UserCharity.objects.get(username=username)
                user_item = list(Need.objects.filter(username=username).values())
                connection_profile = Connect.objects.filter(charity_user=username).values('sponsor_user').annotate(
                    user_count=Count('sponsor_user')).order_by('-user_count')
                for ele in list(connection_profile):
                    connection_list.append(ele['sponsor_user'])
                connection_user = UserSponsor.objects.filter(username__in=connection_list)
            else:  # update table Sponsor and provide
                user_profile = UserSponsor.objects.get(username=username)
                user_item = list(Provide.objects.filter(username=username).values())
                connection_profile = Connect.objects.filter(sponsor_user=username).values('charity_user').annotate(
                    user_count=Count('charity_user')).order_by('-user_count')
                for ele in list(connection_profile):
                    connection_list.append(ele['charity_user'])
                connection_user = UserCharity.objects.filter(username__in=connection_list)

            print(connection_user.values())
            print(username)
        return render(request=request,
                      template_name="cc/details.html",
                      context={"details_found": True,
                               'details_user': user,
                               "details": user_profile,
                               "connection_user": connection_user,  # same as user_profile
                               "item": user_item,
                               'signin_status': signin_status,
                               'current_user': request.user,
                               })

    except Exception as exc:
        return render(request=request,
                      template_name="cc/details.html",
                      context={"details_found": False,
                               'signin_status': signin_status,
                               'current_user': request.user,
                               })


def charity_list(request):
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    if request.method == 'GET':
        form = PageForm
        user_profile = UserCharity.objects.all()[:10]
        page_nums = 1
    else:
        form = PageForm(request.POST)
        page_nums = int(form.data.get('page'))

        # determine which pages should be displayed
        if page_nums > int(math.ceil(UserCharity.objects.count() / 10)):
            user_profile = UserCharity.objects.all()[:10]
        else:
            user_profile = UserCharity.objects.all()[(page_nums - 1) * 10:page_nums * 10]

    user_item = list()
    for user in user_profile.values('username'):
        username = user['username']
        user_item.append(Need.objects.filter(username_id__exact=username).values())
    user_profile = zip(user_profile, user_item)
    return render(request=request,
                  template_name="cc/charity_list.html",
                  context={"lists": user_profile,
                           "form": form,
                           "pages": int(math.ceil(UserCharity.objects.count() / 10)),
                           "page_nums": page_nums,
                           'signin_status': signin_status,
                           'current_user': request.user,
                           }
                  )


def sponsor_list(request):
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    if request.method == 'GET':
        form = PageForm
        user_profile = UserSponsor.objects.all()[:10]
        page_nums = 1
    else:
        form = PageForm(request.POST)
        page_nums = int(form.data.get('page'))

        # determine which pages should be displayed
        if page_nums > int(math.ceil(UserSponsor.objects.count() / 10)):
            user_profile = UserSponsor.objects.all()[:10]
        else:
            user_profile = UserSponsor.objects.all()[(page_nums - 1) * 10:page_nums * 10]

    user_item = list()
    for user in user_profile.values('username'):
        username = user['username']
        user_item.append(Provide.objects.filter(username_id__exact=username).values())

    user_profile = zip(user_profile, user_item)
    return render(request=request,
                  template_name="cc/sponsor_list.html",
                  context={"lists": user_profile,
                           "form": form,
                           "pages": int(math.ceil(UserSponsor.objects.count() / 10)),
                           "page_nums": page_nums,
                           'signin_status': signin_status,
                           'current_user': request.user,
                           })


@login_required
def test_connect(request):
    # fake data
    connect_slug = 'Wilder'
    message_request = 'hello'
    # *** fake data ***

    request_user = request.user
    Message.objects.create(request_user=request_user,
                           reply_user=connect_slug,
                           message_request=message_request)

    return render(request=request,
                  template_name="cc/sponsor_list.html")


@login_required
def test_message(request):
    request_user = request.user
    message_send = list(Message.objects.filter(request_user=request_user).values())
    message_receive_unread = list(Message.objects.filter(reply_user=request_user, message_type=1).values())
    message_receive_read = list(Message.objects.filter(Q(message_type__gt=1), reply_user=request_user).values())
    print(message_send)
    print(message_receive_unread)
    print(message_receive_read)
    # for ele in message_receive_unread:
    #     type_m = ele.message_type
    #     print(type_m)

    return render(request=request,
                  template_name="cc/sponsor_list.html")


@login_required
def test_message_reply(request):
    # fake data
    message_slug = '4'
    message_reply = 'hello too'
    reply_type = True
    # *** fake data ***
    message = Message.objects.get(id=message_slug)
    request_user = message.request_user
    reply_user = message.reply_user
    print(request_user, reply_user)
    if reply_type:
        message.message_reply = message_reply
        message.message_type = 2
        request_user_type = User.objects.get(username=request_user).user_type
        print(request_user_type)

        if request_user_type == 1:
            Connect.objects.create(charity_user=request_user,
                                   sponsor_user=reply_user)
            update_charity = UserCharity.objects.get(username=request_user)
            update_sponsor = UserSponsor.objects.get(username=reply_user)
        else:
            Connect.objects.create(charity_user=reply_user,
                                   sponsor_user=request_user)
            update_charity = UserCharity.objects.get(username=reply_user)
            update_sponsor = UserSponsor.objects.get(username=request_user)
        update_charity.connection += 1
        update_sponsor.connection += 1
        update_charity.save()
        update_sponsor.save()
    else:
        message.message_reply = message_reply
        message.message_type = 3
    message.save()

    return render(request=request,
                  template_name="cc/sponsor_list.html")


@login_required
def test_recommendation(request):
    # fake data
    recommendation_level = 1  # 0:all 1:only 1 or more connect 2:only no connection
    # *** fake data ***

    request_user = request.user
    user_item = list(Need.objects.filter(username=request_user).values())
    print(user_item)
    need_list = []
    for ele in user_item:
        need_list.append(ele['need'])
    print(need_list)
    if need_list:
        sponsor_r = list(Provide.objects.values('username').filter(need__in=need_list).annotate(
            user_count=Count('username')).order_by('-user_count'))
        print(sponsor_r)

    sponsor_r_list = []
    sponsor_r_dict = {}
    for ele in sponsor_r:
        sponsor_r_list.append(ele['username'])
        sponsor_r_dict[ele['username']] = ele['user_count']
    print(sponsor_r_list)
    print(sponsor_r_dict)

    if sponsor_r_list:
        if recommendation_level == 0:
            sponsor_r_profile = list(
                UserSponsor.objects.filter(Q(connection__gte=0), username__in=sponsor_r_list).values('username',
                                                                                                     'long_name'))
        elif recommendation_level == 1:
            sponsor_r_profile = list(
                UserSponsor.objects.filter(Q(connection__gte=1), username__in=sponsor_r_list).values('username',
                                                                                                     'long_name'))
        elif recommendation_level == 2:
            sponsor_r_profile = list(
                UserSponsor.objects.filter(Q(connection=0), username__in=sponsor_r_list).values('username',
                                                                                                'long_name'))
    else:
        sponsor_r_profile = []

    sponsor_r_profile = sorted(sponsor_r_profile, key=lambda x: sponsor_r_list.index(x['username']))
    print(sponsor_r_profile)

    user_item = list()
    for ele in sponsor_r_profile[:10]:
        user_item.append(
            (sponsor_r_dict[ele['username']], Provide.objects.filter(username_id__exact=ele['username']).values()))

    print(user_item)

    return_profile = zip(sponsor_r_profile[:10], user_item)
    for ele in return_profile:
        print(ele[0]['long_name'], ele[1][0], ele[1][1])

    return render(request=request,
                  template_name="cc/sponsor_list.html")


def test_search(request):
    # fake data
    search_name = 'r'
    search_description = 'r'
    search_need = 'o'
    # *** fake data ***

    # result = UserCharity.objects.filter(username__icontains='Frank').first()
    # res = result.need_set.all().values()
    # result = UserCharity.objects.select_related().filter(long_name__icontains='r', need__need='Food').values('username')
    result = UserCharity.objects.select_related().filter(long_name__icontains=search_name,
                                                         description__icontains=search_description,
                                                         need__need__icontains=search_need).values('username',
                                                                                                   'need__need')
    print(result)

    return render(request=request,
                  template_name="cc/sponsor_list.html")


def test_top(request):
    sponsor_t_profile = list(UserSponsor.objects.order_by('-connection').values('username', 'long_name', 'connection'))[
                        :10]
    print(sponsor_t_profile)

    user_item = list()
    for ele in sponsor_t_profile:
        user_item.append(
            (ele['connection'], Provide.objects.filter(username_id__exact=ele['username']).values()))

    print(user_item)

    return_profile = zip(sponsor_t_profile, user_item)
    for ele in return_profile:
        print(ele[0]['long_name'], ele[1][0], ele[1][1])

    return render(request=request,
                  template_name="cc/sponsor_list.html")


@login_required
def connect(request, connect_slug):
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    print(connect_slug)
    if request.method == 'GET':
        form = ConnectForm
        print('aa')
    else:
        form = ConnectForm(request.POST)
        message_request = form.data.get('message')
        request_user = request.user
        Message.objects.create(request_user=request_user,
                               reply_user=connect_slug,
                               message_request=message_request)
        print(request_user)
        print(connect_slug)
        print(message_request)
    return render(request=request,
                  template_name="cc/connect.html",
                  context={'form': form,
                           'signin_status': signin_status,
                           'current_user': request.user,
                           'connect_slug': connect_slug,
                           }
                  )


@login_required
def inbox(request):
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    if request.method == 'GET':
        request_user = request.user
        message_receive_unread = list(Message.objects.filter(reply_user=request_user, message_type=1).values())
        message_receive_read = list(Message.objects.filter(Q(message_type__gt=1), reply_user=request_user).values())
        print(message_receive_unread)
        print(message_receive_read)

    return render(request=request,
                  template_name="cc/inbox.html",
                  context={'signin_status': signin_status,
                           'current_user': request.user,
                           'message_receive_unread': message_receive_unread,
                           'message_receive_read': message_receive_read,
                           }
                  )


@login_required
def outbox(request):
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    if request.method == 'GET':
        request_user = request.user
        message_receive_unread = list(Message.objects.filter(request_user=request_user, message_type=1).values())
        message_receive_read = list(Message.objects.filter(Q(message_type__gt=1), request_user=request_user).values())
        print(message_receive_read)
    return render(request=request,
                  template_name="cc/outbox.html",
                  context={'signin_status': signin_status,
                           'current_user': request.user,
                           'message_receive_unread': message_receive_unread,
                           'message_receive_read': message_receive_read,
                           }
                  )


@login_required
def reply_message(request, message_slug):
    print(f'slug:{message_slug}')
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    message = Message.objects.get(id=message_slug)
    request_user = message.request_user
    reply_user = message.reply_user
    if request.method == 'GET':
        form = MessageForm
    else:
        form = MessageForm(request.POST)
        message_reply = form.data.get('message_reply')
        reply_type = form.data.get('your_reply')
        # print(message_reply)
        # print(reply_type)
        request_user_type = User.objects.get(username=request_user).user_type
        print(request_user_type)
        if int(reply_type) == 2:
            if request_user_type == 1:
                Connect.objects.create(charity_user=request_user,
                                       sponsor_user=reply_user)
                update_charity = UserCharity.objects.get(username=request_user)
                update_sponsor = UserSponsor.objects.get(username=reply_user)
            else:
                Connect.objects.create(charity_user=reply_user,
                                       sponsor_user=request_user)
                update_charity = UserCharity.objects.get(username=reply_user)
                update_sponsor = UserSponsor.objects.get(username=request_user)
            update_charity.connection += 1
            update_sponsor.connection += 1
            update_charity.save()
            update_sponsor.save()
        if int(reply_type) == 3:
            print('failed')
        message.message_reply = message_reply
        message.message_type = int(reply_type)
        message.save()

    return render(request=request,
                  template_name="cc/reply_message.html",
                  context={'signin_status': signin_status,
                           'current_user': request.user,
                           'form': form,
                           'message': message,
                           }
                  )


@login_required
def show_message(request, message_slug):
    print(f'slug:{message_slug}')

    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    message = {}
    if request.method == 'GET':
        message = Message.objects.get(id=message_slug)

    return render(request=request,
                  template_name="cc/show_message.html",
                  context={'signin_status': signin_status,
                           'current_user': request.user,
                           'message': message,
                           }
                  )


@login_required
def recommendation(request):
    request_user = request.user
    user_item = list(Need.objects.filter(username=request_user).values())
    print(user_item)
    need_list = []
    for ele in user_item:
        need_list.append(ele['need'])
    print(need_list)
    if need_list:
        sponsor_r = list(Provide.objects.values('username').filter(need__in=need_list).annotate(
            user_count=Count('username')).order_by('-user_count'))
        print(sponsor_r)

    sponsor_r_list = []
    for ele in sponsor_r:
        sponsor_r_list.append(ele['username'])
    print(sponsor_r_list)

    if sponsor_r_list:
        sponsor_r_profile = list(
            UserSponsor.objects.filter(username__in=sponsor_r_list).values('username', 'long_name', 'website'))
    print(sponsor_r_profile)
    for item in sponsor_r_profile:
        for i in sponsor_r:
            if item['username'] == i['username']:
                item['user_count'] = i['user_count']

    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    if request.method == 'GET':
        form = PageForm

        sponsor_r_profile = sponsor_r_profile[:10]
        page_nums = 1
    else:
        form = PageForm(request.POST)
        page_nums = int(form.data.get('page'))

        # determine which pages should be displayed
        if page_nums > int(math.ceil(len(sponsor_r_profile) / 10)):
            sponsor_r_profile = sponsor_r_profile[:10]
        else:
            sponsor_r_profile = sponsor_r_profile[(page_nums - 1) * 10:page_nums * 10]
        for item in sponsor_r_profile:
            for i in sponsor_r:
                if item['username'] == i['username']:
                    item['user_count'] = i['user_count']
    return render(request=request,
                  template_name="cc/recommendation.html",
                  context={"lists": sponsor_r_profile,
                           "form": form,
                           "pages": int(len(sponsor_r_profile) / 10) + 1,
                           "page_nums": page_nums,
                           'signin_status': signin_status,
                           'current_user': request.user,
                           })

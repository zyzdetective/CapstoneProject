from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from cc.forms import SignupForm, SigninForm, EditForm, ItemForm, PageForm, ConnectForm, MessageForm, RecommendationForm, \
    SearchForm
from cc.models import User, UserCharity, UserSponsor, Need, Provide, Message, Connect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Count
import math, pytz, datetime
from django import forms


# Create your views here.

def base(request):
    # display current user and unread message number
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    request_user = request.user.username
    message_number = len(list(Message.objects.filter(reply_user=request_user, message_type=1).values()))

    return render(request=request,
                  template_name="base/base.html",
                  context={'signin_status': signin_status,
                           'current_user': request.user,
                           'message_number': message_number,
                           }
                  )


def signup(request):
    # display current user and unread message number
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    request_user = request.user.username
    message_number = len(list(Message.objects.filter(reply_user=request_user, message_type=1).values()))

    # signup
    if request.method == 'GET':
        signup_form = SignupForm
    else:
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            username = signup_form.data.get('username')
            email = signup_form.data.get('email')
            password = signup_form.data.get('password')
            user_type = signup_form.data.get('user_type')
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                user_type=user_type,
            )
            # add user
            if int(user_type[0]) == 1:
                charity = UserCharity.objects.create(user=user, username=username, email=email)
            else:
                sponsor = UserSponsor.objects.create(user=user, username=username, email=email)

            # authenticate
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to edit page.
                return redirect("/edit/")
            else:
                return redirect("/home/")

    return render(request=request,
                  template_name="cc/signup.html",
                  context={"form": signup_form,
                           'signin_status': signin_status,
                           'current_user': request.user,
                           'message_number': message_number,
                           }
                  )


def signin(request):
    # display current user and unread message number
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    request_user = request.user.username
    message_number = len(list(Message.objects.filter(reply_user=request_user, message_type=1).values()))

    # signin
    if request.method == 'GET':

        signin_form = SigninForm
    else:
        signin_form = SigninForm(request.POST)
        username = signin_form.data.get('username')
        password = signin_form.data.get('password')

        # authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect("/home/")
        else:
            # Return an 'invalid login' error message.
            return render(request=request,
                          template_name="cc/signin.html",
                          context={"form": signin_form,
                                   "error": "invalid username or password",
                                   'signin_status': signin_status,
                                   'current_user': request.user,
                                   'message_number': message_number,
                                   }
                          )

    return render(request=request,
                  template_name="cc/signin.html",
                  context={"form": signin_form,
                           'signin_status': signin_status,
                           'current_user': request.user,
                           'message_number': message_number,
                           }
                  )


@login_required
def edit(request):
    # display current user and unread message number
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    request_user = request.user.username
    message_number = len(list(Message.objects.filter(reply_user=request_user, message_type=1).values()))

    # edit
    if request.method == 'GET':
        edit_form = EditForm
        item_form = ItemForm
    else:
        user = request.user.username  # this user -> User.username
        user_type = request.user.user_type
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
        items = [ele.casefold().capitalize() for ele in items]

        # set update obj
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
                update_item.objects.create(username_id=user, need=item)

        # finishing update table Need or provide
        return redirect(f'/details/{user}')

    return render(request=request,
                  template_name="cc/add_profile.html",
                  context={"edit_form": edit_form,
                           "user_type": request.user.user_type,
                           "item_form": item_form,
                           'signin_status': signin_status,
                           'current_user': request.user,
                           'message_number': message_number,
                           }
                  )


@login_required
def signout(request):
    out = logout(request)
    return redirect("/signin/")


def details(request, details_slug):
    # display current user and unread message number
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    request_user = request.user.username
    message_number = len(list(Message.objects.filter(reply_user=request_user, message_type=1).values()))

    # details
    try:
        user = User.objects.get(username=details_slug)
        if request.method == 'GET':
            username = user.username
            user_type = user.user_type
            connection_list = []
            if user_type == 1:  # Charity and need
                user_profile = UserCharity.objects.get(username=username)
                user_item = list(Need.objects.filter(username=username).values())
                connection_profile = Connect.objects.filter(charity_user=username).values('sponsor_user').annotate(
                    user_count=Count('sponsor_user')).order_by('-user_count')
                for ele in list(connection_profile):
                    connection_list.append(ele['sponsor_user'])
                connection_user = UserSponsor.objects.filter(username__in=connection_list)
            else:  # Sponsor and provide
                user_profile = UserSponsor.objects.get(username=username)
                user_item = list(Provide.objects.filter(username=username).values())
                connection_profile = Connect.objects.filter(sponsor_user=username).values('charity_user').annotate(
                    user_count=Count('charity_user')).order_by('-user_count')
                for ele in list(connection_profile):
                    connection_list.append(ele['charity_user'])
                connection_user = UserCharity.objects.filter(username__in=connection_list)

            # return connection user with connection time sort
            connection_user = sorted(list(connection_user.values()), key=lambda x: connection_list.index(x['username']))

        return render(request=request,
                      template_name="cc/details.html",
                      context={"details_found": True,
                               'details_user': user,
                               "details": user_profile,
                               "connection_user": connection_user,  # same as user_profile
                               "item": user_item,
                               'signin_status': signin_status,
                               'current_user': request.user,
                               'message_number': message_number,
                               }
                      )

    # no user slug
    except Exception as exc:
        return render(request=request,
                      template_name="cc/details.html",
                      context={"details_found": False,
                               'signin_status': signin_status,
                               'current_user': request.user,
                               'message_number': message_number,
                               }
                      )


def charity_list(request):
    # display current user and unread message number
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    request_user = request.user.username
    message_number = len(list(Message.objects.filter(reply_user=request_user, message_type=1).values()))

    # charity list
    if request.method == 'GET':
        form = PageForm
        user_profile = UserCharity.objects.all()[:9]
        page_nums = 1
    else:
        form = PageForm(request.POST)
        page_nums = int(form.data.get('page'))

        # determine which pages should be displayed
        if (page_nums <= 0) or (page_nums > int(math.ceil(UserCharity.objects.count() / 9))):
            page_nums = 1
            user_profile = UserCharity.objects.all()[:9]
        else:
            user_profile = UserCharity.objects.all()[(page_nums - 1) * 9:page_nums * 9]

    # get charity need
    user_item = list()
    for user in user_profile.values('username'):
        username = user['username']
        user_item.append(Need.objects.filter(username_id__exact=username).values())

    # return user info
    user_profile = zip(user_profile, user_item)

    return render(request=request,
                  template_name="cc/charity_list.html",
                  context={"lists": user_profile,
                           "form": form,
                           "pages": int(math.ceil(UserCharity.objects.count() / 9)),
                           "page_nums": page_nums,
                           'signin_status': signin_status,
                           'current_user': request.user,
                           'message_number': message_number,
                           }
                  )


def sponsor_list(request):
    # display current user and unread message number
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    request_user = request.user.username
    message_number = len(list(Message.objects.filter(reply_user=request_user, message_type=1).values()))

    # sponsor list
    if request.method == 'GET':
        form = PageForm
        user_profile = UserSponsor.objects.all()[:9]
        page_nums = 1
    else:
        form = PageForm(request.POST)
        page_nums = int(form.data.get('page'))

        # determine which pages should be displayed
        if (page_nums <= 0) or (page_nums > int(math.ceil(UserSponsor.objects.count() / 9))):
            page_nums = 1
            user_profile = UserSponsor.objects.all()[:9]
        else:
            user_profile = UserSponsor.objects.all()[(page_nums - 1) * 9:page_nums * 9]

    # get sponsor provide
    user_item = list()
    for user in user_profile.values('username'):
        username = user['username']
        user_item.append(Provide.objects.filter(username_id__exact=username).values())

    # return user info
    user_profile = zip(user_profile, user_item)

    return render(request=request,
                  template_name="cc/sponsor_list.html",
                  context={"lists": user_profile,
                           "form": form,
                           "pages": int(math.ceil(UserSponsor.objects.count() / 9)),
                           "page_nums": page_nums,
                           'signin_status': signin_status,
                           'current_user': request.user,
                           'message_number': message_number,
                           }
                  )


@login_required
def connect(request, connect_slug):
    # display current user and unread message number
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    request_user = request.user.username
    message_number = len(list(Message.objects.filter(reply_user=request_user, message_type=1).values()))

    # default request
    message_request = ''
    # reply user long name
    reply_long = get_obj(connect_slug).long_name

    # request connect
    if request.method == 'GET':
        form = ConnectForm
    else:
        form = ConnectForm(request.POST)
        message_request = form.data.get('message')
        request_user = request.user.username
        # request_time = sydney time when request send
        request_time = datetime.datetime.now(pytz.timezone('Australia/Sydney')).strftime("%Y-%m-%d %H:%M:%S")
        Message.objects.create(request_user=request_user,
                               reply_user=connect_slug,
                               message_request=message_request,
                               request_time=request_time)
        return redirect(f'/details/{connect_slug}')

    return render(request=request,
                  template_name="cc/connect.html",
                  context={'form': form,
                           'signin_status': signin_status,
                           'current_user': request.user,
                           'connect_slug': connect_slug,
                           'message_request': message_request,
                           'message_number': message_number,
                           'reply_long': reply_long,
                           }
                  )


# get charity obj or sponsor obj with username
def get_obj(username):
    user = User.objects.get(username=username)
    user_type = user.user_type
    if user_type == 1:  # Charity
        user_obj = UserCharity.objects.get(username=username)
    else:  # Sponsor
        user_obj = UserSponsor.objects.get(username=username)
    return user_obj


# get return zip info with charity obj or sponsor obj
def get_zip(message_obj):
    obj_list = []
    for ele in message_obj:
        obj_dic = {}
        request_obj = get_obj(ele['request_user'])
        reply_obj = get_obj(ele['reply_user'])
        obj_dic['request_obj'] = request_obj
        obj_dic['reply_obj'] = reply_obj
        obj_list.append(obj_dic)
    return zip(obj_list, message_obj)


@login_required
def message_box(request):
    # set initiate message list
    message_unread_in = []
    message_read_in = []
    message_unread_out = []
    message_read_out = []

    # display current user and unread message number
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    request_user = request.user.username
    message_number = len(list(Message.objects.filter(reply_user=request_user, message_type=1).values()))

    # message box
    if request.method == 'GET':
        # get return info with request user use custom function get_obj() and get_zip()
        request_user = request.user.username

        message_receive_unread_in = list(
            Message.objects.filter(reply_user=request_user, message_type=1).values())
        message_unread_in = get_zip(message_receive_unread_in)

        message_receive_read_in = list(
            Message.objects.filter(Q(message_type__gt=1), reply_user=request_user).values())
        message_read_in = get_zip(message_receive_read_in)

        message_receive_unread_out = list(
            Message.objects.filter(request_user=request_user, message_type=1).values())
        message_unread_out = get_zip(message_receive_unread_out)

        message_receive_read_out = list(
            Message.objects.filter(Q(message_type__gt=1), request_user=request_user).values())
        message_read_out = get_zip(message_receive_read_out)

    return render(request=request,
                  template_name="cc/message_box.html",
                  context={'signin_status': signin_status,
                           'current_user': request.user,
                           'message_receive_unread_in': message_unread_in,
                           'message_receive_read_in': message_read_in,
                           'message_receive_unread_out': message_unread_out,
                           'message_receive_read_out': message_read_out,
                           'message_number': message_number,
                           }
                  )


@login_required
def reply_message(request, message_slug):
    # default reply
    message_reply = ''

    # display current user and unread message number
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    request_user = request.user.username
    message_number = len(list(Message.objects.filter(reply_user=request_user, message_type=1).values()))

    # get message with slug (id)
    message = Message.objects.get(id=message_slug)

    # get long name for charity and sponsor use custom function get_obj()
    request_long = get_obj(message.request_user).long_name
    reply_long = get_obj(message.reply_user).long_name

    # reply message
    request_user = message.request_user
    reply_user = message.reply_user
    if request.method == 'GET':
        form = MessageForm
    else:
        form = MessageForm(request.POST)
        message_reply = form.data.get('message_reply')
        reply_type = form.data.get('your_reply')
        reply_time = datetime.datetime.now(pytz.timezone('Australia/Sydney')).strftime("%Y-%m-%d %H:%M:%S")
        request_user_type = User.objects.get(username=request_user).user_type

        # update connect table and message table by reply type
        if int(reply_type) == 2:  # agree
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
        if int(reply_type) == 3:  # disagree
            pass
        message.message_reply = message_reply
        message.message_type = int(reply_type)
        message.reply_time = reply_time
        message.save()
        return redirect(f'/message_box')

    return render(request=request,
                  template_name="cc/reply_message.html",
                  context={'signin_status': signin_status,
                           'current_user': request.user,
                           'form': form,
                           'message': message,
                           'request_long': request_long,
                           'reply_long': reply_long,
                           'message_reply': message_reply,
                           'message_number': message_number,
                           }
                  )


@login_required
def show_message(request, message_slug):
    # display current user and unread message number
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    request_user = request.user.username
    message_number = len(list(Message.objects.filter(reply_user=request_user, message_type=1).values()))

    # default return info
    message = {}
    request_long = ''
    reply_long = ''

    # show message
    if request.method == 'GET':
        # get message with slug (id)
        message = Message.objects.get(id=message_slug)

        # get long name for charity and sponsor use custom function get_obj()
        request_long = get_obj(message.request_user).long_name
        reply_long = get_obj(message.reply_user).long_name

    return render(request=request,
                  template_name="cc/show_message.html",
                  context={'signin_status': signin_status,
                           'current_user': request.user,
                           'message': message,
                           'request_long': request_long,
                           'reply_long': reply_long,
                           'message_number': message_number,
                           }
                  )


@login_required
def recommendation(request):
    # display current user and unread message number
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    request_user = request.user.username
    message_number = len(list(Message.objects.filter(reply_user=request_user, message_type=1).values()))

    # get request user's need
    request_user = request.user.username
    user_item = list(Need.objects.filter(username=request_user).values())
    need_list = []
    for ele in user_item:
        need_list.append(ele['need'])

    # get recommend sponsor
    if need_list:
        sponsor_r = list(Provide.objects.values('username').filter(need__in=need_list).annotate(
            user_count=Count('username')).order_by('-user_count'))

    # get recommend sponsor info
    sponsor_r_list = []
    sponsor_r_dict = {}
    for ele in sponsor_r:
        sponsor_r_list.append(ele['username'])
        sponsor_r_dict[ele['username']] = ele['user_count']

    # set default page number
    page = 0

    # recommendation display
    if request.method == 'GET':
        page_nums = 1
        recommendation_form = RecommendationForm
        page_form = PageForm

        # get return recommend sponsor info
        if sponsor_r_list:
            sponsor_r_profile = list(
                UserSponsor.objects.filter(Q(connection__gte=0), username__in=sponsor_r_list).values('username',
                                                                                                     'long_name'))
        else:
            sponsor_r_profile = []

        # get all page number
        if len(sponsor_r_profile) / 9 > int(len(sponsor_r_profile) / 9):
            page = int(len(sponsor_r_profile) / 9) + 1
        else:
            page = int(len(sponsor_r_profile) / 9)
        sponsor_r_profile = sorted(sponsor_r_profile, key=lambda x: sponsor_r_list.index(x['username']))[:9]

        # get sponsor provide and number of match need
        user_item = list()
        for ele in sponsor_r_profile:
            user_item.append(
                (sponsor_r_dict[ele['username']], Provide.objects.filter(username_id__exact=ele['username']).values()))

        # get return info
        return_profile = zip(sponsor_r_profile, user_item)
    else:
        # receive page number and recommendation level
        recommendation_form = RecommendationForm(request.POST)
        page_form = PageForm(request.POST)
        recommendation_level = int(recommendation_form.data.get('recommendation_choice'))
        page_nums = int(page_form.data.get('page'))

        # get recommend sponsor by recommendation level
        sponsor_r_profile = list()
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

        # get all page number
        if len(sponsor_r_profile) / 9 > int(len(sponsor_r_profile) / 9):
            page = int(len(sponsor_r_profile) / 9) + 1
        else:
            page = int(len(sponsor_r_profile) / 9)

        # get sponsor provide and number of match need
        user_item = list()
        for ele in sponsor_r_profile:
            user_item.append(
                (sponsor_r_dict[ele['username']], Provide.objects.filter(username_id__exact=ele['username']).values()))

        # determine which pages should be displayed
        if (page_nums <= 0) or (page_nums > math.ceil(len(sponsor_r_profile) / 9)):
            page_nums = 1
            sponsor_r_profile = sponsor_r_profile[:9]
        else:
            sponsor_r_profile = sponsor_r_profile[(page_nums - 1) * 9:page_nums * 9]

    # get return info
    return_profile = zip(sponsor_r_profile, user_item)

    return render(request=request,
                  template_name="cc/recommendation.html",
                  context={"return_profile": return_profile,
                           "page_form": page_form,
                           "recommendation_form": recommendation_form,
                           "pages": page,
                           "page_nums": page_nums,
                           'signin_status': signin_status,
                           'current_user': request.user,
                           'message_number': message_number,
                           }
                  )


# top 10 sponsor everyone can access
def top(request):
    # display current user and unread message number
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    request_user = request.user.username
    message_number = len(list(Message.objects.filter(reply_user=request_user, message_type=1).values()))

    # top 10 sponsor
    if request.method == 'GET':
        sponsor_t_profile = list(
            UserSponsor.objects.order_by('-connection').values('username', 'long_name', 'connection'))[:10]

        # get user sponsor provide
        user_item = list()
        for ele in sponsor_t_profile:
            user_item.append(
                (ele['connection'], Provide.objects.filter(username_id__exact=ele['username']).values()))

        # set return info
        return_profile = zip(sponsor_t_profile, user_item)

    return render(request=request,
                  template_name="cc/top.html",
                  context={"lists": return_profile,
                           'signin_status': signin_status,
                           'current_user': request.user,
                           'message_number': message_number,
                           }
                  )


@login_required
def search(request):
    # display current user and unread message number
    if request.user.is_anonymous:
        signin_status = False
    else:
        signin_status = True
    request_user = request.user.username
    message_number = len(list(Message.objects.filter(reply_user=request_user, message_type=1).values()))

    # default return info
    charity_s_profile = []
    user_item = []
    page = 1

    # search for charity
    if request.method == 'GET':
        search_form = SearchForm
        page_form = PageForm
        page_nums = 1
    else:
        search_form = SearchForm(request.POST)
        search_name = search_form.data.get('name')
        search_description = search_form.data.get('description')
        search_need = search_form.data.get('need')
        page_form = PageForm(request.POST)
        page_nums = int(page_form.data.get('page'))

        # get charity with search requirement (partial matching string for name description and need, case insensitive)
        charity_s_profile = UserCharity.objects.select_related().filter(long_name__icontains=search_name,
                                                                        description__icontains=search_description,
                                                                        need__need__icontains=search_need).distinct().values(
            'username',
            'long_name',
            'description')

        # get all page number
        if len(charity_s_profile) / 9 > int(len(charity_s_profile) / 9):
            page = int(len(charity_s_profile) / 9) + 1
        else:
            page = int(len(charity_s_profile) / 9)

        # get charity need and first 20 characters of description
        user_item = list()
        for ele in charity_s_profile:
            user_item.append(
                (ele['long_name'], ele['description'][:20] + '...',
                 Need.objects.filter(username_id__exact=ele['username']).values()))

        # determine which pages should be displayed
        if (page_nums <= 0) or (page_nums > math.ceil(len(charity_s_profile) / 9)):
            page_nums = 1
            charity_s_profile = charity_s_profile[:9]
        else:
            charity_s_profile = charity_s_profile[(page_nums - 1) * 9:page_nums * 9]

    # get return info
    return_profile = zip(charity_s_profile, user_item)
    return render(request=request,
                  template_name="cc/search.html",
                  context={'signin_status': signin_status,
                           'current_user': request.user,
                           'search_form': search_form,
                           'return_profile': return_profile,
                           'page_form': page_form,
                           "pages": page,
                           "page_nums": page_nums,
                           'message_number': message_number,
                           }
                  )

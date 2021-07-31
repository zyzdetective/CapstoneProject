from django.urls import path, include, re_path
from cc import views

urlpatterns = [
    path('', views.base, name='home'),
    path('home/', views.base, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('edit/', views.edit, name='edit'),
    path('signout/', views.signout, name='signout'),
    path('charity_list/', views.charity_list, name='charity_list'),
    path('sponsor_list/', views.sponsor_list, name='sponsor_list'),
    path('details/<slug:details_slug>', views.details, name='details'),
    path('connect/<slug:connect_slug>', views.connect, name='connect'),
    path('message_box/', views.message_box, name='message_box'),
    path('reply/<slug:message_slug>', views.reply_message, name='reply_message'),
    path('message/<slug:message_slug>', views.show_message, name='show_message'),
    path('recommendation/', views.recommendation, name='recommendation'),
    path('top_sponsors/', views.top, name='top_sponsors'),
    path('search/', views.search, name='search'),
    re_path(r'.*', views.base, name='home'),
]

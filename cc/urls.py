from django.urls import path, include
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
    path('inbox/', views.inbox, name='inbox'),
    path('outbox/', views.outbox, name='outbox'),
    path('inbox_message/', views.inbox_message, name='inbox_message'),
    path('outbox_message/', views.outbox_message, name='outbox_message'),
    # path('message_details/<slug:message_slug>', views.message_details, name='connect'),
]

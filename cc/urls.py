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
    path('reply/<slug:message_slug>', views.reply_message, name='reply_message'),
    path('message/<slug:message_slug>', views.show_message, name='show_message'),
    path('recommendation/', views.recommendation, name='recommendation'),
    path('top_sponsors/', views.top, name='top_sponsors'),
    # path('message_details/<slug:message_slug>', views.message_details, name='connect'),
    # path('test_c/', views.test_connect),
    path('test_m/', views.test_message),
    path('test_m_r/', views.test_message_reply),
    path('test_r', views.test_recommendation),
    path('test_s', views.test_search),
    path('test_t', views.test_top),
]

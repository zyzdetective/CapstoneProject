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
]

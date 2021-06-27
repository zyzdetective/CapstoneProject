from django.urls import path, include
from cc import views

urlpatterns = [
    path('signup/', views.signup),
    path('signin/', views.signin),
    path('edit/', views.edit),
    path('signout/', views.signout),
    path('charity_list/', views.charity_list),
    path('sponsor_list/', views.sposor_list),
    path('details/<slug:details_slug>', views.details,name='details'),
]

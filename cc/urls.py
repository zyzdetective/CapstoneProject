from django.urls import path, include
from cc import views

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('home/', views.home),
    path('sponsor-profile/', views.sponsor_profile),
    path('charity-profile/', views.charity_profile),
]
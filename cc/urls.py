from django.urls import path, include
from cc import views

urlpatterns = [
    path('signup/', views.signup),
    path('signin/', views.signin),
    path('edit/', views.edit),
    path('logout/', views.logout)
]
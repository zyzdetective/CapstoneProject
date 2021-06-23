from django.urls import path, include
from cc import views

urlpatterns = [
    path('signup/', views.signup),
]
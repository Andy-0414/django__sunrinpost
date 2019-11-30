from django.urls import path, include
from .views import login, v_logout, register, getProfile

urlpatterns = [
    path('login/', login),
    path('logout/', v_logout),
    path('register/', register),
    path('getProfile/', getProfile),
]

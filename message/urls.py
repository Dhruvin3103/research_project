
from django.contrib import admin
from django.urls import path,include
from .views import UserMessageAPI,UserIsStressAPI

urlpatterns = [
    path('usermessage/',UserMessageAPI.as_view(),name='users-message'),
    path('userdata/',UserIsStressAPI.as_view(),name='user-data')
]


from django.contrib import admin
from django.urls import path,include
from .views import UserMessageAPI

urlpatterns = [
    path('usermessage/',UserMessageAPI.as_view(),name='users-message')
]

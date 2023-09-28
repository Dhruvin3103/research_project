from django.contrib import admin
from django.urls import path,include
from .views import UserMessageAPI,UserIsStressAPI,FormScoreAPI,CSVAPI


urlpatterns = [
    path('usermessage/',UserMessageAPI.as_view(),name='users-message'),
    path('userdata/',UserIsStressAPI.as_view(),name='user-data'),
    path('csv/',CSVAPI.as_view(),name='csv'),
    path('formscore/',FormScoreAPI.as_view(),name='form-score'),
]


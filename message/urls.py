from django.contrib import admin
from django.urls import path,include
from .views import UserMessageAPI,UserIsStressAPI,MessageCSVAPI
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('usermessage/',UserMessageAPI.as_view(),name='users-message'),
    path('userdata/',UserIsStressAPI.as_view(),name='user-data'),
    path('messagecsv/',MessageCSVAPI.as_view(),name='mess-csv')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
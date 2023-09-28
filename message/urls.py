from django.contrib import admin
from django.urls import path,include
from .views import UserMessageAPI,UserIsStressAPI,FormScoreAPI,CSVAPI
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('usermessage/',UserMessageAPI.as_view(),name='users-message'),
    path('userdata/',UserIsStressAPI.as_view(),name='user-data'),
    path('csv/',CSVAPI.as_view(),name='csv'),
    path('formscore/',FormScoreAPI.as_view(),name='form-score')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
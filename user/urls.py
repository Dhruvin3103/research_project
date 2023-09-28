from django.urls import path,include
from .views import CheckAdminAPI

urlpatterns = [
    path('checkadmin/',CheckAdminAPI.as_view(),name='check-admin')
]


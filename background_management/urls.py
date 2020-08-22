from django.urls import path
from .views import *

urlpatterns=[
    path('management.user',UserManagementView.as_view(),name='user_management')
]
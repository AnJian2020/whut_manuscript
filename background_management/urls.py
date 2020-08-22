from django.urls import path
from .views import *

urlpatterns=[
    path('management.user',UserManagementView.as_view(),name='user_management'),
    path('management.information',UserInformationView.as_view(),name='user_information'),
    path('management.group',UserGroupPermissionView.as_view(),name='user_group'),
    path('management.permission',PermissionView.as_view(),name="group_permission")
]
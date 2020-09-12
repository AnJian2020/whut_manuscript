from django.urls import path
from .views import *

urlpatterns=[
    path('user',UserManagementView.as_view(),name='user_management'),
    path('information',UserInformationView.as_view(),name='user_information'),
    path('group',UserGroupPermissionView.as_view(),name='user_group'),
    path('permission',PermissionView.as_view(),name="group_permission")
]
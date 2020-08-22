from django.urls import path
from .views import *

urlpatterns=[
    path('user.login',LoginView.as_view(),name='login'),
    path('user.logout',LogoutView.as_view(),name='logout'),
    path('user.register',RegisterView.as_view(),name='register'),
    path('user.information',PersonalInformationView.as_view(),name='information'),
    path('user.changepassword',ChangePassword.as_view(),name='changepassword')
]
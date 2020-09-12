from django.urls import path
from .views import *

urlpatterns=[
    path('login',LoginView.as_view(),name='login'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('register',RegisterView.as_view(),name='register'),
    path('information',PersonalInformationView.as_view(),name='information'),
    path('changepassword',ChangePassword.as_view(),name='changepassword')
]
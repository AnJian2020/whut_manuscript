from django.contrib import admin
from .models import UserInformation
from django.contrib.auth.models import Permission

admin.site.register(UserInformation)
admin.site.register(Permission)


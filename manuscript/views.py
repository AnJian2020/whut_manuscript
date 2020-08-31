from .models import ManuscriptModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

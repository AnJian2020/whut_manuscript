import os
from random import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Permission
from django.contrib.auth import login, logout, authenticate
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from .models import UserInformation, UserToken
from django.views.decorators.csrf import csrf_exempt
from .modelSerializer import UserInformationSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    去除 CSRF 检查
    """

    def enforce_csrf(self, request):
        return


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """
    用户登录视图
    """
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        userLoginData = request.data
        username = userLoginData['username']
        password = userLoginData['password']
        user = User.objects.filter(username=username)
        if user:
            userAuthent = authenticate(username=username, password=password)
            if userAuthent:
                if userAuthent.is_active:
                    login(request, userAuthent)
                user_id = user[0].id
                token = UserToken.objects.filter(user_id=user_id)
                if token:
                    token.delete()
                UserToken.objects.create(user_id=user_id)
                token = UserToken.objects.filter(user_id=user_id)[0].key
                return Response(status=200,
                                data={'code': 200, 'message': 'success', 'token': token, 'username': username})
            else:
                return Response(status=200, data={'code': 404, 'message': 'Wrong user name or password.'})
        else:
            return Response(status=200, data={'code': 404, 'message': "Wrong user name or password."})


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    """
    用户注册视图
    """
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data['username']
        email = data['email']
        password = data['password']
        user = User.objects.filter(username=username)
        if user:
            return Response(status=200, data={'code': 404, 'message': "User is already registered."})
        else:
            try:
                newUser = User.objects.create_user(username=username, email=email, password=password)
                UserInformation.objects.create(username=username)
                # UserInformation.objects.create(username=username)
                return Response(status=200, data={'message': 'User registration succeeded.'})
            except:
                return Response(status=404, data={'message': 'User registration failed.'})


class LogoutView(APIView):
    """
    用户退出登录视图
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        logout(request)
        return Response(status=200, data={'message': "logout"})


@method_decorator(csrf_exempt, name='dispatch')
class ChangePassword(APIView):
    """
    用户更改密码
    """
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    def put(self, request):
        data = request.data
        user = User.objects.filter(username=data['username']).first()
        if user and user.email:
            if not request.session.get('code', None):
                code = chr(random.randint(65, 91)) + str(random.randint(1000, 9999))
                request.session['code'] = code
                with open(os.path.join(os.getcwd(), os.path.join('user', 'code.txt')), 'r', encoding='utf-8') as f:
                    content = f.read()
                content = content % code
                user.email_user('密码修改', content)
                return Response(status=200,
                                data={'message': 'The verification code was sent successfully.'})
            else:
                if data['code'] and request.session.get('code', None) != data['code']:
                    return Response(status=204, data={'message': 'Verification code input error.'})
                elif data['code'] and request.session.get('code', None) == data['code']:
                    newPassword = make_password(data['password'], None, 'pbkdf2_sha256')
                    user.password = newPassword
                    user.save()
                    del request.session['code']
                    return Response(status=200, data={'message': 'Password changed successfully.'})
        else:
            return Response(status=404, data={'message': 'The user is not registered or unbound.'})


class PersonalInformationView(APIView):
    """
    用户个人信息视图
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """
        用户修改个人信息
        :param request:
        :return:
        """
        userInformationData = request.data
        username = userInformationData['username']
        operation = UserInformation.objects.filter(username=username).first()
        serializer = UserInformationSerializer()

        if operation:
            serializer.update(operation, userInformationData)
            return Response(status=200, data={'message': 'Data updated successfully.'})
        else:
            # serializer.save()
            # return Response(status=200,data={'message':'ok'})
            return Response(status=200, data={'message': 'Data update failed.'})

    def get(self, request):
        """
        用户查看个人信息
        :param request:
        :return:
        """
        username = request.user
        user = UserInformation.objects.filter(username=username)
        if user:
            pageNumberPagination = PageNumberPagination()
            page = pageNumberPagination.paginate_queryset(queryset=user, request=request, view=self)
            serializer = UserInformationSerializer(instance=page, many=True)
            return Response(status=200, data=serializer.data)
        else:
            return Response(status=204,
                            data={'message': "This user information is not available."})

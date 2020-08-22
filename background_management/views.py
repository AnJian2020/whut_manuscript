from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User, Group, Permission
from .modelSerializer import UserSerializer, UserInformationSerializer
from user.models import UserInformation
import datetime


class UserManagementView(APIView):
    """
    用户管理视图
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [DjangoModelPermissions, IsAuthenticated, IsAdminUser]
    queryset = User.objects.all()

    def put(self, request):
        """
        修改用户信息（用户名，密码，邮箱）
        :param request:
        :return:
        """
        self.__data = request.data
        self.__username = self.__data.get('username', None)
        self.__user = User.objects.filter(username=self.__username)
        self.__serializer = UserSerializer(data=self.__data)
        if self.__serializer.is_valid():
            if self.__user:
                self.__serializer.update(self.__user, self.__data)
                return Response(status=200, data={'code': 200, 'message': 'Data updated successfully.'})
            else:
                return Response(status=200, data={'code': 200, 'message': 'User not registered.'})
        return Response(status=200, data={'code': 200, 'message': 'Data update failed.'})

    def get(self, request):
        """
        查看用户信息
        :param request:
        :return:
        """
        self.__user = User.objects.all().order_by('id')
        if self.__user:
            pageNumberPagination = PageNumberPagination()
            page = pageNumberPagination.paginate_queryset(queryset=self.__user, request=request, view=self)
            serializer = UserSerializer(instance=page, many=True)
            return Response(status=200, data=serializer.data)
        return Response(status=200, data={'code': 200, 'message': 'Data is empty.'})

    def post(self, request):
        """
        添加新用户
        :param request:
        :return:
        """
        self.__newUserData = request.data
        self.__username = self.__newUserData.get('username', None)
        oldUser = User.objects.filter(username=self.__username)
        self.__newUserData['date_joined'] = datetime.datetime.now()
        serializer = UserSerializer(data=self.__newUserData)
        if serializer.is_valid():
            if oldUser:
                return Response(status=200, data={'code': 200, 'message': 'User already exists.'})
            else:
                serializer.save()
                return Response(status=200, data={'code': 200, 'message': 'User added successfully.'})
        return Response(status=200, data={'code': 200, 'message': 'User added failed.'})

    def delete(self, request):
        """
        删除用户
        :param request:
        :return:
        """
        self.__username = request.data.get('username', None)
        if self.__username:
            User.objects.filter(username=self.__username).delete()
            return Response(status=200, data={'code0': 200, 'message': 'User deleted successfully.'})
        return Response(status=200, data={'code': 200, 'message': 'User deleted failed.'})


class UserInformationView(APIView):
    """
    用户信息管理视图
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [DjangoModelPermissions, IsAuthenticated, IsAdminUser]
    queryset = User.objects.all()

    def get(self, request):
        """
        查看用户信息数据
        :param request:
        :return: response
        """
        self.__userInformation = UserInformation.objects, all().order_by('username')
        if self.__userInformation:
            pageNumberPagination = PageNumberPagination()
            page = pageNumberPagination.paginate_queryset(queryset=self.__userInformation, request=request, view=self)
            serializer = UserInformationSerializer(instance=page, many=True)
            return Response(status=200, data={'code': 200, 'data': serializer.data})
        return Response(status=200, data={'code': 200, 'message': 'Data is empty.'})

    def post(self, request):
        """
        添加用户信息
        :param request:
        :return:
        """
        self.__newUserInformation = request.data
        self.__username = self.__newUserInformation.get('username', None)
        if self.__username:
            self.__oldUser = UserInformation.objects.filter()
            if self.__oldUser:
                return Response(status=200, data={'code': 200, 'message': "User's information already exists."})
            else:
                serializer = UserInformationSerializer(data=self.__newUserInformation)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=200, data={'code': 200, 'message': "User's information added successly."})
                return Response(status=200,
                                data={'code': 200, 'message': 'The data submitted did not meet the requirements.'})
        return Response(status=200,
                        data={'code': 200, 'message': "User information already exists, no need to submit."})

    def put(self, request):
        """
        修改用户信息
        :param request:
        :return:
        """
        self.__userInformation=request.data
        self.__username=self.__userInformation.get('username',None)
        self.__user=UserInformation.objects.filter(username=self.__username)
        if not self.__user:
            return Response(status=200,data={'code':200,'message':'User information does not exist.'})
        else:
            serializer=UserInformationSerializer(data=self.__userInformation)
            if serializer.is_valid():
                serializer.update(self.__user,self.__userInformation)
                return Response(status=200,data={'code':200,'message':"The user's information was updated successfully."})
            return Response(status=200,data={'code':200,'message':"The data submitted did not meet the requirements."})




    def delete(self, request):
        """
        删除用户信息
        """


class UserGroupPermissionView(APIView):
    """
    用户组及其权限管理视图
    """


class PermissionView(APIView):
    """
    系统权限管理
    """

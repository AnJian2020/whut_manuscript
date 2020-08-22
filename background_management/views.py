from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User, Group, Permission
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from .modelSerializer import UserSerializer, UserInformationSerializer, GroupSerializer, PermissionSerializer
from user.models import UserInformation
import datetime


# @method_decorator(permission_required(perm='user.vip_user'),name='dispatch')
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
        self.__userInformation = UserInformation.objects.all().order_by('username')
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
        self.__userInformation = request.data
        self.__username = self.__userInformation.get('username', None)
        self.__user = UserInformation.objects.filter(username=self.__username)
        if not self.__user:
            return Response(status=200, data={'code': 200, 'message': 'User information does not exist.'})
        else:
            serializer = UserInformationSerializer(data=self.__userInformation)
            if serializer.is_valid():
                serializer.update(self.__user, self.__userInformation)
                return Response(status=200,
                                data={'code': 200, 'message': "The user's information was updated successfully."})
            return Response(status=200,
                            data={'code': 200, 'message': "The data submitted did not meet the requirements."})

    def delete(self, request):
        """
        删除用户信息
        """
        self.__username = request.data.get('username', None)
        if self.__username:
            UserInformation.objects.filter(username=self.__username).delete()
            return Response(status=200, data={'code0': 200, 'message': 'User deleted successfully.'})
        return Response(status=200, data={'code': 200, 'message': 'User deleted failed.'})


class UserGroupPermissionView(APIView):
    """
    用户组及其权限管理视图
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [DjangoModelPermissions, IsAuthenticated, IsAdminUser]
    queryset = Group.objects.all()

    def get(self, request):
        """
        查看用户组及其权限
        :param request:
        :return:
        """
        self.__searchGroup = request.data.get('searchGroup', None)
        if self.__searchGroup:
            self.__allGroup = Group.objects.filter(name=self.__searchGroup).order_by('id')
        else:
            self.__allGroup = Group.objects.all().order_by("id")
        if self.__allGroup:
            pageNumberPagination = PageNumberPagination()
            page = pageNumberPagination.paginate_queryset(queryset=self.__allGroup, request=request, view=self)
            serializer = GroupSerializer(instance=page, many=True)
            response_data = serializer.data
            for item in range(len(serializer.data)):
                permissions_id = serializer.data[item]['permissions']
                response_data[item]['permissions'] = []
                for permission_id in permissions_id:
                    permission = Permission.objects.filter(id=permission_id).first()
                    response_data[item]['permissions'].append(
                        dict(id=permission.id, permission_name=permission.name,
                             permission_codename=permission.codename))
            return Response(status=200, data={'code': 200, 'message': response_data})
        return Response(status=200, data={'code': 200, 'message': "Data acquisition failed."})

    def post(self, request):
        """
        创建用户组，并且赋予其相应的权限
        :param request:
        :return:
        """


    def put(self, request):
        """
        修改用户组及其拥有的权限
        :param request:
        :return:
        """

    def delete(self, request):
        """
        删除用户组
        :param request:
        :return:
        """


class PermissionView(APIView):
    """
    系统权限管理
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [DjangoModelPermissions, IsAuthenticated, IsAdminUser]
    queryset = Permission.objects.all()

    def post(self, request):
        """
        通过ContenType表和model或者model的实例来寻找ContentType类型
        :param request:
        :return:
        """
        self.__permissionData = request.data
        # permissionModel=self.__permissionData.get('permissionData','Permission')
        codename = self.__permissionData.get('codename', None)
        name = self.__permissionData.get('name', None)
        content_type = ContentType.objects.get_for_model(Permission)
        if Permission.objects.filter(codename=codename):
            return Response(status=200, data={'code': 200, 'message': 'The permission already exists.'})
        if codename and name:
            permission = Permission.objects.create(codename=codename, name=name, content_type=content_type)
            return Response(status=200, data={'code': 200, 'message': 'Permission added successfully.'})
        else:
            return Response(status=200, data={'code': 200, 'message': 'Permission added failed.'})

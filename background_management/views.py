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
        searchUser=request.data.get("searchUser",None)
        if searchUser:
            self.__user=User.objects.filter(username=searchUser).order_by('id')
        else:
            self.__user = User.objects.all().order_by('id')
        if self.__user:
            pageNumberPagination = PageNumberPagination()
            page = pageNumberPagination.paginate_queryset(queryset=self.__user, request=request, view=self)
            serializer = UserSerializer(instance=page, many=True)
            return Response(status=200, data={'allData':len(self.__user),'data':serializer.data})
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
        searchUser=request.data.get("searchUser",None)
        if searchUser:
            self.__userInformation=UserInformation.objects.filter(username=searchUser).order_by('id')
        else:
            self.__userInformation = UserInformation.objects.all().order_by('username')
        if self.__userInformation:
            pageNumberPagination = PageNumberPagination()
            page = pageNumberPagination.paginate_queryset(queryset=self.__userInformation, request=request, view=self)
            serializer = UserInformationSerializer(instance=page, many=True)
            return Response(status=200, data={'allData': len(self.__userInformation), 'data': serializer.data})
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
        defaultPermission = ['add_userinformation', 'change_userinformation', 'view_userinformation',
                             'delete_userinformation', 'add_usertoken', 'change_usertoken', 'change_usertoken',
                             'delete_usertoken']
        self.__groupData = request.data
        self.__groupName = self.__groupData.get('name', None)
        if self.__groupName:
            self.__group = Group.objects.filter(name=self.__groupName)
            if not self.__group:
                serializer = GroupSerializer(data=self.__groupData)
                if serializer.is_valid():
                    serializer.save()
                    newgroup = Group.objects.filter(name=self.__groupName).first()
                    for item in defaultPermission:
                        permission = Permission.objects.get(codename=item)
                        newgroup.permissions.add(permission)
                    return Response(status=200, data={'code': 200, 'message': "Group's information added successly.",
                                                      'new_group_permissions': defaultPermission})
                else:
                    return Response(status=200,
                                    data={'code': 200, 'message': 'The data submitted did not meet the requirements.'})
            else:
                return Response(status=200,
                                data={'code': 200, 'message': "Group'information already exists, no need to submit."})
        else:
            return Response(status=200,
                            data={'code': 200, 'message': "The data submitted did not meet the requirements."})

    def put(self, request):
        """
        修改用户组及其拥有的权限
        :param request:
        :return:
        """
        defaultPermission = ['add_userinformation', 'change_userinformation', 'view_userinformation',
                             'delete_userinformation', 'add_usertoken', 'change_usertoken', 'change_usertoken',
                             'delete_usertoken']
        self.__newGroupData = request.data
        modifyOrganizationInformation = self.__newGroupData.get("modifyOrganizationInformation", None)
        modifyOrganizationPermission = self.__newGroupData.get("modifyOrganizationPermission", None)
        oldGroupName = self.__newGroupData.get('old_group_name', None)
        newGroupName = self.__newGroupData.get('new_group_name', None)
        if modifyOrganizationInformation:
            if oldGroupName != newGroupName and oldGroupName and newGroupName:
                group = Group.objects.filter(name=oldGroupName)
                IsTheNewNameUsed = Group.objects.filter(name=newGroupName)
                if group and not IsTheNewNameUsed:
                    group.update(name=newGroupName)
                else:
                    return Response(status=200, data={'code': 200,
                                                      'message': "The user group does not exist or the organization name is already occupied."})
            groupName = newGroupName
        else:
            groupName = oldGroupName
        if modifyOrganizationPermission:
            newGroupPermissions = self.__newGroupData.get("newGroupPermissions", [])
            group = Group.objects.get(name=groupName)
            group.permissions.clear()
            newGroupPermissions.extend(defaultPermission)
            permissionCanBeAdded = Permission.objects.values('codename')
            canAddPermissions = [item['codename'] for item in permissionCanBeAdded]
            for item in newGroupPermissions:
                if item in canAddPermissions:
                    permission = Permission.objects.get(codename=item)
                    group.permissions.add(permission)
                else:
                    return Response(status=200, data={'code': 200,
                                                      'message': "The added permissions do not meet the requirements."})
        return Response(status=200, data={"code": 200, "message": "Data updated successfully."})

    def delete(self, request):
        """
        删除用户组。这里不确定是否需要将户组内的用户先移除后，再删除用户。
        :param request:
        :return:
        """
        self.__groupName = request.data.get('group_name', None)
        if self.__groupName:
            try:
                group = Group.objects.get(name=self.__groupName)
                group.permissions.clear()
                group.delete()
                return Response(status=200, data={'code': 200, "message": "User group deleted successfully"})
            except Exception as e:
                return Response(status=200, data={'code': 200, 'message': "User group deletion failed.Error:" + e})
        return Response(status=200, data={'code': 200, 'message': "User group deletion failed."})


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

    def get(self, request):
        """
        查看系统所有权限
        :param request:
        :return:
        """
        searchPermission = request.data.get('searchPermission')
        if searchPermission:
            self.__allPermissions = Permission.objects.filter(codename=searchPermission).order_by('id')
        else:
            self.__allPermissions = Permission.objects.all().order_by('id')
        if self.__allPermissions:
            pageNumberPagination = PageNumberPagination()
            page = pageNumberPagination.paginate_queryset(queryset=self.__allPermissions, request=request, view=self)
            serializer = PermissionSerializer(many=True, instance=page)
            return Response(status=200, data={"allData": len(self.__allPermissions), "data": serializer.data})
        return Response(status=200, data={'code': 200, "message": "Data is empty."})

    def delete(self,request):
        deletePermissionName=request.data.get('deletePermissionName')
        if deletePermissionName:
            Permission.objects.filter(codename=deletePermissionName).delete()
            return Response(status=200,data={'code':200,'message':"Permission deleted successfully."})
        return Response(status=200,data={'code':200,"message":"Permission deleted failed."})

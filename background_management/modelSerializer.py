from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.hashers import make_password
from datetime import datetime
from user.models import UserInformation


class UserSerializer(Serializer):
    """
    用户模型序列化
    """
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)
    email = serializers.EmailField()
    date_joined = serializers.DateTimeField(default=datetime.now())

    def create(self, validated_data):
        """
        添加新的用户
        :param validated_data:
        :return:
        """
        self.__username = validated_data.get('username', None)
        self.__email = validated_data.get('email', None)
        self.__password = validated_data.get('password', None)
        return User.objects.create_user(username=self.__username, email=self.__email, password=self.__password)

    def update(self, instance, validated_data):
        """
        修改用户信息，在修改用户密码时需要进行加密处理
        :param instance:
        :param validated_data:
        :return:
        """
        self.__password = validated_data.get('password', None)
        newPassword = make_password(self.__password, None, 'pbkdf2_sha256')
        validated_data['password'] = newPassword
        return instance.update(**validated_data)


class UserInformationSerializer(serializers.ModelSerializer):
    """
    用户信息模型序列化
    """

    class Meta:
        model = UserInformation
        fields = "__all__"



class GroupSerializer(serializers.ModelSerializer):
    """
    用户组模型序列化
    """

    class Meta:
        model = Group
        fields = "__all__"


class PermissionSerializer(serializers.ModelSerializer):
    """
    权限序列化
    """

    class Meta:
        model = Permission
        fields = "__all__"

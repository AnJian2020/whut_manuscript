from .models import UserInformation
from rest_framework import serializers


class UserInformationSerializer(serializers.ModelSerializer):
    """
    用户信息模型序列化
    """
    class Meta:
        model = UserInformation
        fields = "__all__"

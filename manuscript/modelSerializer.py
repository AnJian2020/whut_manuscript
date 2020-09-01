from .models import *
from rest_framework import serializers


class SubjectSerializer(serializers.ModelSerializer):
    """
    研究方向模型序列化
    """
    class Meta:
        model = SubjectModel
        fields = "__all__"

class ContributionTypeSerializer(serializers.ModelSerializer):
    """
    投稿类型模型序列化
    """
    class Meta:
        model=ContributionTypeModel
        fields="__all__"

class TradeSerializer(serializers.ModelSerializer):
    """
    行业领域模型序列化
    """
    class Meta:
        model=TradeModel
        fields="__all__"




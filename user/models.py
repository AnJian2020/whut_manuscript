from django.db import models
from rest_framework.authtoken.models import Token
from datetime import datetime,timedelta
from NEWS_Manage.settings import *

class UserInformation(models.Model):
    """
    用户信息模型
    """
    username = models.CharField(max_length=150, primary_key=True, verbose_name='用户账号')
    real_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='真实姓名')
    contact_way = models.CharField(max_length=64, blank=True, null=True, verbose_name='联系方式')
    adress = models.CharField(max_length=128, blank=True, null=True, verbose_name='家庭地址')
    postal_code = models.CharField(max_length=12, null=True, blank=True, verbose_name='邮编')
    birthday = models.DateField(blank=True, null=True, verbose_name='出生日期')
    sex = models.BooleanField(blank=True, null=True, verbose_name='性别')
    education = models.CharField(max_length=64, null=True, blank=True, verbose_name='学历')
    country = models.CharField(max_length=128, null=True, blank=True, verbose_name='国家')
    province = models.CharField(max_length=128, null=True, blank=True, verbose_name='省份')
    city = models.CharField(max_length=128, null=True, blank=True, verbose_name='城市')
    work_unit = models.CharField(max_length=256, null=True, blank=True, verbose_name='工作单位')
    resume = models.TextField(null=True, blank=True, verbose_name='个人简介')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户信息表"
        verbose_name_plural = "用户信息表"

        permissions=(

        )

class UserToken(Token):
    """
    继承Token模型。并添加token过期时间
    """
    outTime=models.DateTimeField(default=datetime.now()+timedelta(minutes=TOKEN_OUT_TIME))

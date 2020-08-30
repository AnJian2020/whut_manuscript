import os
from django.apps import AppConfig

default_app_config = 'user.UserConfig'

def getCurretnAppName(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class UserConfig(AppConfig):
    name = getCurretnAppName(__file__)
    verbose_name = "用户模块"

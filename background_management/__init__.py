import os
from django.apps import AppConfig

default_app_config = "background_management.BackgroundManagementConfig"


def getCurrentAppName(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class BackgroundManagementConfig(AppConfig):
    name = getCurrentAppName(__file__)
    verbose_name = "后台管理"

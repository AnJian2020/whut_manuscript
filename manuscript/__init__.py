import os
from django.apps import AppConfig

default_app_config = "manuscript.ManuscriptConfig"


def getCurrentAppName(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class ManuscriptConfig(AppConfig):
    name = getCurrentAppName(__file__)
    verbose_name = "稿件模块"

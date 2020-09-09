"""
author xuhao
time 2020-08-30
"""
from django.urls import path
from .views import *

urlpatterns=[
    path("subject",SubjectView.as_view(),name="subject"),
    path("contributionType",ContributionTypeView.as_view(),name="contributionType"),
    path("trade",TradeView.as_view(),name="trade"),
    path("manuscript",ManuscriptView.as_view(),name="manuscript")
]
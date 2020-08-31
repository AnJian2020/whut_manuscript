"""
@author xuhao
@time 2020-08-30
"""

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class SubjectModel(models.Model):
    """
    研究方向模型
    """
    id = models.AutoField(_("subject id"), primary_key=True)
    name = models.CharField(_("subject name"), max_length=150)
    add_time = models.DateTimeField(_("add time"), default=timezone.now())

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _("subject")
        verbose_name_plural = _("subject")


class ContributionTypeModel(models.Model):
    """
    投稿类型模型
    """
    id = models.AutoField(_("contribution id"), primary_key=True)
    name = models.CharField(_("contribution name"), max_length=120)
    add_time = models.DateTimeField(_("add time"), default=timezone.now())

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _("contribution")
        verbose_name_plural = _("contribution")


class TradeModel(models.Model):
    """
    行业领域模型
    """
    id = models.AutoField(_("trade"), primary_key=True)
    name = models.CharField(_("trade name"), max_length=120)
    add_time = models.DateTimeField(_("add time"), default=timezone.now())

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _("trade")
        verbose_name_plural = _("trade")


class ManuscriptModel(models.Model):
    """
    稿件信息模型
    """
    manuscript_id = models.CharField(_("manuscript id"), max_length=18, primary_key=True)
    title = models.CharField(_("manuscript title"), max_length=256)
    author = models.CharField(_("author name"), max_length=128)
    abstract = models.TextField(_("abstract"))
    textOfManuscript = models.TextField(_("text of manuscript"))
    reference = models.TextField(_("reference"))
    corresponding_author = models.CharField(_("corresponding author"), max_length=150)
    corresponding_author_contact_way = models.CharField(_("contact information of corresponding author"), max_length=64)
    subject = models.ManyToManyField(
        SubjectModel,
        verbose_name=_("subject"))
    contribution_type = models.ManyToManyField(
        ContributionTypeModel,
        verbose_name=_("contribution type"))
    trade = models.ManyToManyField(
        TradeModel,
        verbose_name=_("trade"))
    memory_way = models.CharField(_("memory way"), max_length=256)
    contribution_time = models.DateTimeField(default=timezone.now(), verbose_name=_("delivery time"))

    def __str__(self):
        return self.manuscript_id

    class Meta:
        verbose_name = _("manuscript")
        verbose_name_plural = _("manuscript")

        permissions = (
            ('change_oneself_manuscript', 'Can change oneself manuscript'),
            ('delete_oneself_manuscript', 'Can delete oneself manuscript'),
            ('view_onesef_manuscript', 'Can view oneself manuscript')
        )


class CheckManuscriptModel(models.Model):
    """
    稿件检测模型
    """
    id = models.CharField(_("check id"), max_length=18, primary_key=True)
    check_name = models.CharField(_("check name"), max_length=150)
    check_contact_way = models.CharField(_("contact way"), max_length=64)
    duplicate_checking_rate = models.FloatField(_("duplicate checking rate"))
    multiple_contributions_to_one_manuscript = models.BooleanField(_("multiple contributions to one manuscript"))
    is_subject = models.BooleanField(_("subject"))
    is_contribution = models.BooleanField(_("contribution"))
    is_trade = models.BooleanField(_("trade"))
    check_result = models.CharField(_("check result"), max_length=256)
    check_time = models.DateTimeField(_("check time"), default=timezone.now())

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = _("check")
        verbose_name_plural = _("check")


class ReviewManuscriptModel(models.Model):
    """
    稿件审核模型
    """
    id=models.CharField(_("review id"),max_length=18,primary_key=True)





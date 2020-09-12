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
    add_time = models.DateTimeField(_("add time"), default=timezone.now)

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
    add_time = models.DateTimeField(_("add time"), default=timezone.now)

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
    add_time = models.DateTimeField(_("add time"), default=timezone.now)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _("trade")
        verbose_name_plural = _("trade")


class CheckManuscriptModel(models.Model):
    """
    稿件检测模型
    """
    check_id = models.CharField(_("check id"), max_length=18, primary_key=True)
    # manuscript = models.OneToOneField(
    #     ManuscriptModel,
    #     on_delete=models.CASCADE,
    #     verbose_name=_("manuscript"))
    check_name = models.CharField(_("check name"), max_length=150, blank=True, null=True)
    check_contact_way = models.CharField(_("contact way"), max_length=64, blank=True, null=True)
    duplicate_checking_rate = models.FloatField(_("duplicate checking rate"), null=True, blank=True)
    multiple_contributions_to_one_manuscript = models.BooleanField(_("multiple contributions to one manuscript"),
                                                                   null=True, blank=True)
    is_subject = models.BooleanField(_("subject"), null=True, blank=True)
    is_contribution = models.BooleanField(_("contribution"), blank=True, null=True)
    is_trade = models.BooleanField(_("trade"), blank=True, null=True)
    check_status = models.CharField(_("check status"), max_length=16, blank=True, null=True)
    check_time = models.DateTimeField(_("check time"), default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.check_id

    class Meta:
        verbose_name = _("check")
        verbose_name_plural = _("check")


class ReviewManuscriptModel(models.Model):
    """
    稿件审核模型
    """
    review_id = models.CharField(_("review id"), max_length=18, primary_key=True)
    # manuscript = models.OneToOneField(
    #     ManuscriptModel,
    #     on_delete=models.CASCADE,
    #     verbose_name=_("manuscript"))
    # 初审
    preliminary_status = models.CharField(_("preliminary status"), max_length=16, null=True, blank=True)
    preliminary_evaluation = models.TextField(_("preliminary evaluation"), null=True, blank=True)
    preliminary_user = models.CharField(_("preliminary user"), max_length=150, null=True, blank=True)
    preliminary_user_contact_way = models.CharField(_('preliminary user contact way'), max_length=64, null=True,
                                                    blank=True)
    preliminary_time = models.DateTimeField(_("preliminary time"), null=True, blank=True)
    preliminary_deadline = models.DateTimeField(_("preliminary deadline"), null=True, blank=True)
    # 外审
    # 外审只是参考，无法决定稿件是否通过，故暂时取消外审结果字段
    # external_audit_status=models.CharField(_('external audit status'),max_length=16,null=True,blank=True)
    external_audit_evaluation = models.TextField(_("external audit evaluation"), null=True, blank=True)
    external_audit_user = models.CharField(_("external audit user"), max_length=150, null=True, blank=True)
    external_audit_user_contact_way = models.CharField(_("external audit user contact way"), max_length=64, null=True,
                                                       blank=True)
    external_audit_time = models.DateTimeField(_("external audit time"), null=True, blank=True)
    external_audit_deadline = models.DateTimeField(_("external audit deadline"), null=True, blank=True)
    # 复审
    review_status = models.CharField(_("review status"), max_length=16, null=True, blank=True)
    review_evaluation = models.TextField(_("review evaluation"), null=True, blank=True)
    review_user = models.CharField(_("review user"), max_length=150, null=True, blank=True)
    review_user_contact_way = models.CharField(_("review user contact way"), max_length=64, null=True, blank=True)
    review_time = models.DateTimeField(_("review time"), null=True, blank=True)
    review_deadline = models.DateTimeField(_("review deadline"), null=True, blank=True)
    # 终审
    final_judgment_status = models.CharField(_("final judgment status"), max_length=16, null=True, blank=True)
    final_judgment_evaluation = models.TextField(_("final judgment evaluation"), null=True, blank=True)
    final_judgment_user = models.CharField(_("final judgment user"), max_length=150, null=True, blank=True)
    final_judgment_user_contact_way = models.CharField(_("final judgment user contact way"), max_length=64, null=True,
                                                       blank=True)
    final_judgment_time = models.DateTimeField(_("final judgment time"), null=True, blank=True)
    final_judgment_deadline = models.DateTimeField(_("final judgment deadline"), null=True, blank=True)

    def __str__(self):
        return self.review_id

    class Meta:
        verbose_name = _("review")
        verbose_name_plural = _("review")


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
    memory_way = models.CharField(_("memory way"), max_length=256, null=True, blank=True)
    contribution_time = models.DateTimeField(default=timezone.now, verbose_name=_("delivery time"))
    check_status = models.OneToOneField(
        CheckManuscriptModel,
        on_delete=models.CASCADE,
        verbose_name=_("manuscript inspection"),
        null=True, blank=True
    )
    review_status = models.OneToOneField(
        ReviewManuscriptModel,
        on_delete=models.CASCADE,
        verbose_name=_("manuscript review"),
        null=True, blank=True
    )

    def __str__(self):
        return self.manuscript_id

    class Meta:
        verbose_name = _("manuscript")
        verbose_name_plural = _("manuscript")

        permissions = (
            ('change_oneself_manuscript', 'Can change oneself manuscript'),
            ('delete_oneself_manuscript', 'Can delete oneself manuscript'),
            ('view_oneself_manuscript', 'Can view oneself manuscript')
        )

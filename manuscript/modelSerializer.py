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
        model = ContributionTypeModel
        fields = "__all__"


class TradeSerializer(serializers.ModelSerializer):
    """
    行业领域模型序列化
    """

    class Meta:
        model = TradeModel
        fields = "__all__"


class CheckManuscriptSerializer(serializers.ModelSerializer):
    """
    稿件检测模型序列化
    """

    class Meta:
        model = CheckManuscriptModel
        fields = "__all__"


class ReviewManuscriptSerializer(serializers.ModelSerializer):
    """
    稿件审核模型序列化
    """

    class Meta:
        model = ReviewManuscriptModel
        fields = "__all__"


class ManuscriptSerializer(serializers.ModelSerializer):
    """
    稿件信息模型序列化
    """

    review_status = ReviewManuscriptSerializer()
    check_status = CheckManuscriptSerializer()


    class Meta:
        model = ManuscriptModel
        fields = "__all__"

    def create(self, validated_data):
        """
        重写create方法，将获取的稿件数据存储到对应的数据表中
        :param validated_data:
        :return:
        """
        newManuscriptData = validated_data
        check_status = validated_data.get("check_status", None)
        review_status = validated_data.get("review_status", None)
        check_id = check_status.get("check_id", None)
        review_id = review_status.get("review_id", None)
        isCheck = CheckManuscriptModel.objects.filter(check_id=check_id).first()  #查看稿件审核记录表中是否存在有记录，没有则生成对应记录
        isReview = ReviewManuscriptModel.objects.filter(review_id=review_id).first()
        # nowTime = datetime.now()
        if not isCheck:
            # newCheckID = "CH" + str(nowTime.year) + str(nowTime.month) + str(nowTime.day) + str(nowTime.hour) + str(
            #     nowTime.minute) + str(nowTime.second)
            isCheck =CheckManuscriptModel.objects.create(**check_status)
        if not isReview:
            isReview=ReviewManuscriptModel.objects.create(**review_status)
        newManuscriptData['check_status']=isCheck
        newManuscriptData['review_status']=isReview
        manyToManyData=dict()
        manyToManyData['subject']=newManuscriptData['subject']
        newManuscriptData.pop('subject')
        manyToManyData['trade']=newManuscriptData['trade']
        newManuscriptData.pop("trade")
        manyToManyData['contribution_type']=newManuscriptData['contribution_type']
        newManuscriptData.pop('contribution_type')
        manuscript=ManuscriptModel.objects.create(**newManuscriptData)
        manuscript.trade.set(manyToManyData['trade'])
        manuscript.subject.set(manyToManyData['subject'])
        manuscript.contribution_type.set(manyToManyData['contribution_type'])
        return manuscript

    def update(self, instance, validated_data):
        """
        更新稿件信息，多对多数据只能进行添加和删除，不能进行修改，只有非关系字段或者外键可以进行更新.
        用户修改稿件信息，只能修改稿件的作者，内容等，不能修改稿件的检测与审核信息
        :param instance:
        :param validated_data:
        :return:
        """
        newManuscriptData=validated_data
        manyToManyData = dict()

        # oneToOneData=dict()
        # oneToOneData['check_status'] = newManuscriptData['check_status']
        # newManuscriptData.pop('check_status')
        # oneToOneData['review_status'] = newManuscriptData['review_status']
        # newManuscriptData.pop("review_status")

        manyToManyData['subject'] = newManuscriptData['subject']
        newManuscriptData.pop('subject')
        manyToManyData['trade'] = newManuscriptData['trade']
        newManuscriptData.pop("trade")
        manyToManyData['contribution_type'] = newManuscriptData['contribution_type']
        newManuscriptData.pop('contribution_type')

        manuscript_id = validated_data.get("manuscript_id", None)
        manuscript=ManuscriptModel.objects.filter(manuscript_id=manuscript_id)
        manuscript.update(**validated_data)

        manuscript[0].trade.set(manyToManyData['trade'])
        manuscript[0].subject.set(manyToManyData['subject'])
        manuscript[0].contribution_type.set(manyToManyData['contribution_type'])

        return manuscript

        # check_status = validated_data.get("check_status", None)
        # review_status = validated_data.get("review_status", None)
        # check_id = check_status.get("check_id", None)
        # review_id = review_status.get("review_id", None)
        # isCheck = CheckManuscriptModel.objects.filter(check_id=check_id)  # 查看稿件审核记录表中是否存在有记录，没有则生成对应记录
        # isReview = ReviewManuscriptModel.objects.filter(review_id=review_id)
        # # updateManuscriptData=validated_data
        # if isCheck and isReview:
        #     # isCheck.update(**check_status)
        #     # isReview.update(**review_status)
        #     manuscript_id=validated_data.get("manuscript_id",None)
        #     # updateManuscriptData['check_status']=isCheck
        #     # updateManuscriptData['review_status']=isReview
        #     return ManuscriptModel.objects.filter(manuscript_id=manuscript_id).update(**newManuscriptData)
        # elif not isCheck and isReview:
        #     isReview.update(**review_status)
        #     manuscript_id = validated_data.get("manuscript_id", None)
        #     updateManuscriptData['review_status'] = isReview
        #     return ManuscriptModel.objects.filter(manuscript_id=manuscript_id).update(**updateManuscriptData)
        # elif isCheck and not isReview:
        #     isCheck.update(**check_status)
        #     manuscript_id = validated_data.get("manuscript_id", None)
        #     updateManuscriptData['check_status']=isCheck
        #     return ManuscriptModel.objects.filter(manuscript_id=manuscript_id).update(**updateManuscriptData)
        #
        #


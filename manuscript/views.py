from .models import SubjectModel, ContributionTypeModel, TradeModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from .modelSerializer import SubjectSerializer, ContributionTypeSerializer, TradeSerializer
from datetime import datetime


class SubjectView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # @permission_required(perm="manuscript.add_subjectmodel")
    # 因为每个用户都可以直接获取subject的内容，但是只有特定用户才能添加、修改、删除subject，
    # 故无法通过为视图类添加装饰器实现，而单独为方法添加装饰器则会报错。
    def post(self, request):
        if request.user.has_perm("manuscript.add_subjectmodel"):
            subjectName = request.data.get('subjectName', None)
            if subjectName:
                subject = SubjectModel.objects.filter(name=subjectName)
                if not subject:
                    serializer = SubjectSerializer(data=dict(name=subjectName))
                    if serializer.is_valid():
                        serializer.save()
                        return Response(status=200, data={"message": "Data inserted successfully."})
                    return Response(status=404, data=serializer.errors)
                return Response(status=403, data={"message": "Data already exists."})
            return Response(status=204, data={"message": "Data is empty."})
        else:
            return Response(status=404, data={"message": "The user does not have this permission."})

    def delete(self, request):
        if request.user.has_perm("manuscript.delete_subjectmodel"):
            subjectName = request.data.get("subjectName", None)
            if subjectName:
                subject = SubjectModel.objects.filter(name=subjectName)
                if not subject:
                    subject.delete()
                    return Response(status=200, data={"message": "Data deleted successfully."})
                return Response(status=403, data={"message": "Data does not exist."})
            return Response(status=204, data={"message": "Data is empty."})
        else:
            return Response(status=404, data={"message": "The user does not have this permission."})

    def get(self, request):
        allSubject = SubjectModel.objects.all().order_by("id")
        if allSubject:
            pageNumberPagination = PageNumberPagination()
            page = pageNumberPagination.paginate_queryset(queryset=allSubject, request=request, view=self)
            serializer = SubjectSerializer(instance=page, many=True)
            return Response(status=200, data={"allData": len(allSubject), "data": serializer.data})
        return Response(status=204, data={"message": "Data is empty."})

    def put(self, request):
        return Response(status=403, data={"message": "Denial of service."})


class ContributionTypeView(APIView):
    """
    投稿类型视图
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # 添加新的投稿类型
    def post(self, request):
        if request.user.has_perm("manuscript.add_contributiontypemodel"):
            newContributionTypeName = request.data.get("contributionType", None)
            if newContributionTypeName:
                contributionType = ContributionTypeModel.objects.filter(name=newContributionTypeName)
                if contributionType:
                    return Response(status=403, data={"message": "Data already exists."})
                serializer = ContributionTypeSerializer(data=dict(name=newContributionTypeName))
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=200, data={"message": "Data inserted successfully."})
                return Response(status=404, data=serializer.errors)
            return Response(status=204, data={'message': "Data is empty."})
        return Response(status=404, data={"message": "The user does not have this permission."})

    # 删除投稿类型
    def delete(self, request):
        if request.user.has_perm("manuscript.delete_contributiontypemodel"):
            contributionTypeName = request.data.get("contributionTypeName", None)
            if contributionTypeName:
                contributionType = ContributionTypeModel.objects.filter(name=contributionTypeName)
                if contributionType:
                    contributionType.delete()
                    return Response(status=200, data={"message": "Data deleted successfully."})
                return Response(status=403, data={"message": "Data does not exist."})
            return Response(status=204, data={"message": "Data is empty."})
        else:
            return Response(status=404, data={"message": "The user does not have this permission."})

    # 查看投稿类型
    def get(self, request):
        allContributionType = ContributionTypeModel.objects.all()
        if allContributionType:
            pageNumberPagination = PageNumberPagination()
            page = pageNumberPagination.paginate_queryset(queryset=allContributionType, request=request, view=self)
            serializer = ContributionTypeSerializer(instance=page, many=True)
            return Response(status=200, data={"allData": len(allContributionType), "data": serializer.data})
        return Response(status=204, data={"message": "Data is empty."})

    # 修改投稿类型，不过项目不需要对投稿类型类型修改
    def put(self, request):
        return Response(status=403, data={"message": "Denial of service."})


class TradeView(APIView):
    """
    行业领域视图
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # 添加新的行业领域
    def post(self, request):
        if request.user.has_perm("manuscript.add_trademodel"):
            newTradeName = request.data.get("tradeName")
            if newTradeName:
                trade = TradeModel.objects.filter(name=newTradeName)
                if trade:
                    return Response(status=403, data={"message": "Data already exists."})
                serializer = TradeSerializer(data=dict(name=newTradeName))
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=200, data={"message": "Data inserted successfully."})
                return Response(status=404, data=serializer.errors)
            return Response(status=204, data={'message': "Data is empty."})
        return Response(status=404, data={"message": "The user does not have this permission."})

    # 删除行业领域
    def delete(self, request):
        if request.user.has_perm("manuscript.delete_trademodel"):
            deleteTradeName = request.data.get("tradeName", None)
            if deleteTradeName:
                deleteTrade = TradeModel.objects.filter(name=deleteTradeName)
                if deleteTrade:
                    deleteTrade.delete()
                    return Response(status=200, data={"message": "Data deleted successfully."})
                return Response(status=403, data={"message": "Data does not exist."})
            return Response(status=204, data={"message": "Data is empty."})
        else:
            return Response(status=404, data={"message": "The user does not have this permission."})

    # 查看系统现有的行业领域
    def get(self, request):
        allTrade = TradeModel.objects.all()
        if allTrade:
            pageNumberPagination = PageNumberPagination()
            page = pageNumberPagination.paginate_queryset(queryset=allTrade, request=request, view=self)
            serializer = TradeSerializer(instance=page, many=True)
            return Response(status=200, data={"allData": len(allTrade), "data": serializer.data})
        return Response(status=204, data={"message": "Data is empty."})

    # 修改行业领域，不过项目不需要对行业领域修改
    def put(self, request):
        return Response(status=403, data={"message": "Denial of service."})


class ManuscriptView(APIView):
    """
    稿件的投递、查看等，根据不同的用户权限进行不同的处理
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        newManuscriptNeedDataField=['title','author','abstract','textOfManuscript','reference','corresponding_author',
                                    'corresponding_author_contact_way','subject','contribution_type','trade',
                                    'contribution_time']
        newManuscriptData = request.data
        for item in newManuscriptNeedDataField:
            if newManuscriptData.get(item) is None:
                return Response(status=403, data={"message": "The data does not meet the requirements."})
        nowTime = datetime.now()
        newManuscriptData['manuscript_id'] = "M" + str(nowTime.year) + str(nowTime.month) + str(nowTime.day) + str(
            nowTime.hour) + str(nowTime.minute) + str(nowTime.second)



    def delete(self, request):
        pass

    def get(self, request):
        pass

    def put(self, request):
        pass

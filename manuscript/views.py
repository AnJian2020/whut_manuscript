from .models import SubjectModel, ContributionTypeModel, TradeModel, ManuscriptModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from user.models import UserInformation
# from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from .modelSerializer import SubjectSerializer, ContributionTypeSerializer, TradeSerializer, ManuscriptSerializer
from datetime import datetime
import os
import re


class SubjectView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # @permission_required(perm="manuscript.add_subjectmodel")
    # 因为每个用户都可以直接获取subject的内容，但是只有特定用户才能添加、修改、删除subject，
    # 故无法通过为视图类添加装饰器实现，而单独为方法添加装饰器则会报错。
    def post(self, request):
        if request.user.has_perm("manuscript.add_subjectmodel"):
            subjectName = request.data.get('name', None)
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
            subjectName = request.data.get("name", None)
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
            newContributionTypeName = request.data.get("name", None)
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
            contributionTypeName = request.data.get("name", None)
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
            newTradeName = request.data.get("name")
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
            deleteTradeName = request.data.get("name", None)
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
        newManuscriptNeedDataField = ['title', 'author', 'abstract', 'textOfManuscript', 'reference',
                                      'corresponding_author',
                                      'corresponding_author_contact_way', 'subject', 'contribution_type', 'trade',
                                      'contribution_time']
        newManuscriptData = request.data
        for item in newManuscriptNeedDataField:
            if newManuscriptData.get(item) is None:
                return Response(status=403, data={"message": "The data does not meet the requirements."})
        nowTime = datetime.now()
        # 稿件提交之时，系统就自动生成稿件编号、稿件审核编号、稿件检测编号
        newManuscriptData['manuscript_id'] = "M" + str(nowTime.year) + str(nowTime.month) + str(nowTime.day) + str(
            nowTime.hour) + str(nowTime.minute) + str(nowTime.second)
        newManuscriptData['check_status']['id'] = "C" + str(nowTime.year) + str(nowTime.month) + str(nowTime.day) + str(
            nowTime.hour) + str(nowTime.minute) + str(nowTime.second)
        newManuscriptData['review_status']['id'] = "R" + str(nowTime.year) + str(nowTime.month) + str(
            nowTime.day) + str(
            nowTime.hour) + str(nowTime.minute) + str(nowTime.second)
        serializer = ManuscriptSerializer(data=newManuscriptData)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data={"message": "Data inserted successfully."})
        return Response(status=404, data={"message": "Data inserted failed."})

    def delete(self, request):
        nowUser = request.user
        deleteManuscript = request.data.get("title", None)
        if nowUser.has_perm("manuscript.delete_oneself_manuscript"):
            userRealName = UserInformation.objects.filter(username=nowUser).first().real_name
            manuscript = ManuscriptModel.objects.filter(Q(corresponding_author=userRealName) | Q(author=userRealName),
                                                        title=deleteManuscript)
        elif nowUser.has_perm("manuscript.delete_manuscriptmodel"):
            manuscript = ManuscriptModel.objects.filter(title=deleteManuscript)
        else:
            return Response(status=404, data={"message": "You do not have permission to delete the data."})
        if manuscript:
            manuscript.delete()
            return Response(status=200, data={'message': "Data deleted successfully."})
        else:
            return Response(status=204, data={"message": "Data is empty."})

    def get(self, request):
        nowUser = request.user
        if nowUser.has_perm("manuscript.view_oneself_manuscript"):
            searchManuscript = request.data.get("title", None)
            userRealName = UserInformation.objects.filter(username=nowUser).first()
            if searchManuscript is None and userRealName:
                userManuscript = ManuscriptModel.objects.filter(
                    Q(corresponding_author=userRealName.real_name) | Q(author=userRealName.real_name)).order_by(
                    "manuscript_id")
            else:
                userManuscript = ManuscriptModel.objects.filter(
                    Q(corresponding_author=userRealName.real_name) | Q(author=userRealName.real_name),
                    Q(title=searchManuscript) | Q(subject=searchManuscript) | Q(trade=searchManuscript)).order_by(
                    "manuscript_id")
        elif nowUser.has_perm("manuscript.view_manuscriptmodel"):
            userManuscript = ManuscriptModel.objects.all().order_by("manuscript_id")
        pageNumberPagination = PageNumberPagination()
        page = pageNumberPagination.paginate_queryset(queryset=userManuscript, request=request, view=self)
        serializer = ManuscriptSerializer(instance=page, many=True)
        return Response(status=200, data={"dataLength": len(userManuscript), "userManuscript": serializer.data})

    def put(self, request):
        nowUser = request.user
        changeManuscript = request.data.get("title", None)
        if nowUser.has_perm("manuscript.change_oneself_manuscript"):
            # 普通用户只能对自己投递的稿件进行相应的修改，这里应该为未进行检测或者审核的稿件才能进行相应的修改,目前问题比较复杂
            userRealName = UserInformation.objects.filter(username=nowUser).first().real_name
            manuscript = ManuscriptModel.objects.filter(Q(author=userRealName) | Q(corresponding_author=userRealName),
                                                        title=changeManuscript)
        elif nowUser.has_perm("manuscript.change_manuscriptmodel"):
            manuscript = ManuscriptModel.objects.filter(title=changeManuscript)
        else:
            return Response(status=404, data={"message": "You do not have permission to delete the data."})
        if manuscript:
            serializer = ManuscriptSerializer(data=request.data)
            if serializer.is_valid():
                serializer.update()
                return Response(status=200, data={"message": "Data modified successfully."})
            return Response(status=204, data={"message": "The data does not meet the requirements."})
        else:
            return Response(status=404, data={"message": "The modified data does not exist."})


class ManuscriptDocumentView(APIView):
    """
    负责稿件文件的上传以及格式审核，稿件名按照title+文件格式的要求，pdf、docx文件
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    documentPath = os.path.join(os.getcwd(), 'document')

    def post(self, request):
        fileDict = request.FILES
        for key, value in fileDict.items():
            fileData = request.FILES.getlist(key)
            for file in fileData:
                filename = file._get_name()
                manuscriptTitle = re.search("^[\u4E00-\u9FA5A-Za-z0-9]{0,}", filename)[0]
                if re.search(".pdf", filename) is None and re.search(".docx", filename) is None:
                    return Response(status=404, data={"message": "The file format does not meet the requirements."})
                if manuscriptTitle:
                    manuscript = ManuscriptModel.objects.filter(title=manuscriptTitle)
                    if manuscript:
                        # 文件上传
                        f = open(os.path.join(self.documentPath, filename), 'wb+')
                        for chunk in file.chunks():
                            f.write(chunk)
                        f.close()
                        newManuscriptPath = os.path.join(self.documentPath, filename)
                        manuscript.update(memory_way=newManuscriptPath)
                        return Response(status=200, data={"message": "The file was uploaded successfully."})
                    return Response(status=204, data={
                        "message": "Failed to upload the manuscript, the information is not perfect, please upload again after improving the manuscript information."})
                else:
                    return Response(status=204, data={"message": "The file format does not meet the requirements."})

    def delete(self, request):
        pass


class ManuscriptCheckView(APIView):
    """
    稿件检测视图
    """


class ManuscriptReviewView(APIView):
    """
    稿件的审核，包括初审、外审、复审和终审
    """

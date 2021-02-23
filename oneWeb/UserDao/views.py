#coding:utf-8
# Create your views here.
from UserDao.models import *
from rest_framework import filters
from UserDao.UserDaoSer import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.response import APIResponse,getUser,MyModelViewSet
from utils.tokenCheck import JWTAuthentication
from utils.Pagination import LargeResultsSetPagination



class ProjectViewSet(MyModelViewSet):
    '''
    create:
    创建项目
    retrieve:
    获取项目详情数据
    update:
    完整更新项目
    destroy:
    删除项目
    list:
    获取项目列表数据
    search:name
    搜索姓名
    '''
    authentication_classes = [JWTAuthentication, ]
    queryset = Project.objects.filter(delete=1).order_by('-createTime')
    serializer_class = ProjectSer
    pagination_class = LargeResultsSetPagination
    #搜索
    filter_backends = [filters.SearchFilter]
    #搜索关键字
    search_fields = ['name']

#登陆获取token接口
class LoginAPIView(APIView):
    #登陆接口禁用一切认证和权限
    authentication_classes = []
    permission_classes = []
    def post(self,request,*args,**kwargs):
        userObj = LoginSerializer(data=request.data)
        userObj.is_valid(raise_exception=True)

        return Response(data={'msg':'登陆成功','username':userObj.user.username,'token':userObj.token},status=status.HTTP_200_OK)


class GlobalVariableViewSet(MyModelViewSet):
    '''
    create:
    创建项目
    retrieve:
    获取项目详情数据
    update:
    完整更新项目
    destroy:
    删除项目
    list:
    获取项目列表数据
    search:name
    搜索姓名
    '''

    authentication_classes = [JWTAuthentication, ]
    queryset = GlobalVariable.objects.filter(delete=1).order_by('-createTime')
    serializer_class = GlobalVariableSer
    pagination_class = LargeResultsSetPagination
    #搜索
    filter_backends = [filters.SearchFilter]
    #搜索关键字
    search_fields = ['name']

class GlobalVariable_extViewSet(MyModelViewSet):
    '''
    create:
    创建项目
    retrieve:
    获取项目详情数据
    update:
    完整更新项目
    destroy:
    删除项目
    list:
    获取项目列表数据
    search:key，=globalId
    搜索
    '''
    authentication_classes = [JWTAuthentication, ]
    queryset = GlobalVariable_ext.objects.filter().order_by('-id')
    serializer_class = GlobalVariable_extSer
    pagination_class = LargeResultsSetPagination
    #搜索
    filter_backends = [filters.SearchFilter]
    #搜索关键字
    search_fields = ['key','=globalId']

class TestCaseViewSet(MyModelViewSet):
    '''
    create:
    创建项目
    retrieve:
    获取项目详情数据
    update:
    完整更新项目
    destroy:
    删除项目
    list:
    获取项目列表数据
    search:name，=testCaseType
    搜索
    '''
    authentication_classes = [JWTAuthentication, ]
    queryset = TestCase.objects.filter(delete=1).order_by('-createTime')
    serializer_class = TestCaseSer
    pagination_class = LargeResultsSetPagination
    #搜索
    filter_backends = [filters.SearchFilter]
    #搜索关键字
    search_fields = ['name','=testCaseType']

class TestCaseSepViewSet(MyModelViewSet):
    '''
    create:
    创建项目
    retrieve:
    获取项目详情数据
    update:
    完整更新项目
    destroy:
    删除项目
    list:
    获取项目列表数据
    search:name，=TestCaseId
    搜索
    '''
    authentication_classes = [JWTAuthentication, ]
    queryset = TestCaseSep.objects.filter().order_by('-id')
    serializer_class = TestCaseSepSer
    pagination_class = LargeResultsSetPagination
    #搜索
    filter_backends = [filters.SearchFilter]
    #搜索关键字
    search_fields = ['name','=TestCaseId']

class TestCaseResultTotalViewSet(MyModelViewSet):
    '''
    create:
    创建项目
    retrieve:
    获取项目详情数据
    update:
    完整更新项目
    destroy:
    删除项目
    list:
    获取项目列表数据
    search:projectName
    搜索
    '''
    authentication_classes = [JWTAuthentication, ]
    queryset = TestCaseResultTotal.objects.filter().order_by('-createTime')
    serializer_class = TestCaseResultTotalSer
    pagination_class = LargeResultsSetPagination
    #搜索
    filter_backends = [filters.SearchFilter]
    #搜索关键字
    search_fields = ['projectName']

class TestCaseResultViewSet(MyModelViewSet):
    '''
    create:
    创建项目
    retrieve:
    获取项目详情数据
    update:
    完整更新项目
    destroy:
    删除项目
    list:
    获取项目列表数据
    search:name，=Total_Id
    搜索
    '''
    authentication_classes = [JWTAuthentication, ]
    queryset = TestCaseResult.objects.filter().order_by('-id')
    serializer_class = TestCaseResultSer
    pagination_class = LargeResultsSetPagination
    #搜索
    filter_backends = [filters.SearchFilter]
    #搜索关键字
    search_fields = ['name','=Total_Id']

class TestCaseResult_extViewSet(MyModelViewSet):
    '''
    create:
    创建项目
    retrieve:
    获取项目详情数据
    update:
    完整更新项目
    destroy:
    删除项目
    list:
    获取项目列表数据
    search:name，=testResult_id
    搜索
    '''
    authentication_classes = [JWTAuthentication, ]
    queryset = TestCaseResult_ext.objects.filter().order_by('-createTime')
    serializer_class = TestCaseResult_extSer
    pagination_class = LargeResultsSetPagination
    #搜索
    filter_backends = [filters.SearchFilter]
    #搜索关键字
    search_fields = ['name','=testResult_id']

class Project_TestCaseViewSet(MyModelViewSet):
    '''
    create:
    创建项目
    retrieve:
    获取项目详情数据
    update:
    完整更新项目
    destroy:
    删除项目
    list:
    获取项目列表数据
    search:=projectId,=testId,=id
    搜索
    '''
    authentication_classes = [JWTAuthentication, ]
    queryset = Project_TestCase.objects.filter().order_by('-createTime')
    serializer_class = Project_TestCaseSer
    pagination_class = LargeResultsSetPagination
    #搜索
    filter_backends = [filters.SearchFilter]
    #搜索关键字
    search_fields = ['=projectId','=testId','=id']
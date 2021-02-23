from django.conf.urls import url,include
from UserDao import views
from rest_framework.urlpatterns import format_suffix_patterns
from UserDao.views import *
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.schemas import get_schema_view


router = DefaultRouter()
router.register(r'projects',views.ProjectViewSet)
router.register(r'globalVariables',views.GlobalVariableViewSet)
router.register(r'globalVariable_exts',views.GlobalVariable_extViewSet)
router.register(r'testcases',views.TestCaseViewSet)
router.register(r'testCaseSeps',views.TestCaseSepViewSet)
router.register(r'testCaseResultTotal',views.TestCaseResultTotalViewSet)
router.register(r'testCaseResult',views.TestCaseResultViewSet)
router.register(r'testCaseResult_ext',views.TestCaseResult_extViewSet)
router.register(r'project_TestCase',views.Project_TestCaseViewSet)

schema_view = get_schema_view(title='Test API')

urlpatterns = [
    url(r'^',include(router.urls)),
    url('^schema/$',schema_view),
]
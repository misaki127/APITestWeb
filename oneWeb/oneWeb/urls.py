"""oneWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from APITestWeb import views
from django.conf.urls import include,url

from UserDao import views as Uviews
from UserDao import urls as Uurls

from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import ObtainJSONWebToken,obtain_jwt_token,verify_jwt_token,refresh_jwt_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.documentation import include_docs_urls

schema_view = get_schema_view(
    openapi.Info(
        title="API接口文档平台",    # 必传
        default_version='v1',   # 必传
        description="这是一个接口文档",
        terms_of_service="http://api.wanghan.site",
        contact=openapi.Contact(email="1559284050@qq.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),   # 权限类
)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^dao/testcase/',include(Uurls)),
    url('^schema/$',schema_view),
    path('api-auth/', include('rest_framework.urls',namespace='rest_framework')),  # drf 认证url
    #drf-jwt三个视图接口
    #签发token
    url(r'^obtain/$',obtain_jwt_token),
    #校验token
    url(r'^verify/$',verify_jwt_token),
    #刷新token
    url(r'^refresh/$',refresh_jwt_token),
    url(r'^login/$',Uviews.LoginAPIView.as_view()),
    path('docs/', include_docs_urls(title='测试平台接口文档')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('upload/',views.upload),
    path('download/',views.download_template),
    path('download/use/',views.download_user),
    path('getCodeFile/',views.getCodeFile),
    path('uploadFile/',views.upload),
    path('download/report/',views.download_report),
    path('runTest/download/',views.download_code),
     path('login/',Uviews.logins),
    path('index/',Uviews.index),
    path('login/',auth_views.LoginView.as_view()),
    path('logout/',Uviews.logouts),
    path('createUser/',Uviews.createUser),
    path('remakePassword/',Uviews.remakePassword),
    path('forgetPassword/',Uviews.forgetPassword),
    path('runTestCase/',views.RunTestCase),
]


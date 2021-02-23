#序列化程序
#coding:utf-8

from rest_framework import serializers
from UserDao.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import re

from rest_framework.serializers import ValidationError
from rest_framework_jwt.serializers import jwt_payload_handler,jwt_encode_handler

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username','password')

    def validate(self, attrs):
        #多方式登陆
        user = self.__many__method__login(**attrs)
        print(user)
        #通过user对象生成payload荷载
        payload = jwt_payload_handler(user)
        #通过payload签发token
        token = jwt_encode_handler(payload)

        #将user和token放入序列化对象中
        self.user = user
        self.token = token
        return attrs

    def __many__method__login(self,**attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        #使用正则匹配判断用户输入信息
        #判断邮箱
        if re.match(r'.*@.*',username):
            user = User.objects.filter(email=username).first()
        #判断手机号
        elif re.match(r'^1[3-9][0-9]{9}$',username):
            user = User.objects.filter(mobile=username).first()
        #用户名登陆
        else:
            user = User.objects.filter(username=username).first()

        if not user:
            raise ValidationError({'username':'账号错误'})
        if not user.check_password(password):
            raise ValidationError({'password':'账号错误'})
        return user

class ProjectSer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id','name','userName','user','createTime','delete')#注册表内的字段

class GlobalVariableSer(serializers.ModelSerializer):
    class Meta:
        model = GlobalVariable
        fields = ('id','name','user','userName','delete','createTime')

class GlobalVariable_extSer(serializers.ModelSerializer):
    class Meta:
        model = GlobalVariable_ext
        fields = ('id','key','value','globalId','createTime')

class TestCaseSer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ('id','name','user','userName','testCaseType','delete','createTime')

class TestCaseSepSer(serializers.ModelSerializer):
    class Meta:
        model = TestCaseSep
        fields = ('id','name','url','method','headers','token','findVariable','nameVariable','expectResult','maxTime','waitTime','index','TestCaseId','paramsd','datad','jsond','filesd')

class TestCaseResultTotalSer(serializers.ModelSerializer):
    class Meta:
        model = TestCaseResultTotal
        fields = ('id','projectName','passNums','failNums','errNums','createTime','times','user','userName')

class TestCaseResultSer(serializers.ModelSerializer):
    class Meta:
        model = TestCaseResult
        fields = ('id','name','passNums','failNums','errNums','times','Total_Id')

class TestCaseResult_extSer(serializers.ModelSerializer):
    class Meta:
        model = TestCaseResult_ext
        fields = ('id','name','url','method','headers','paramsd','datad','jsond','filesd','response','code','result','testResult_id','createTime')

class Project_TestCaseSer(serializers.ModelSerializer):
    class Meta:
        model = Project_TestCase
        fields = ('id','projectId','testId','createTime')
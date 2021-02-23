from django.db import models
from django.contrib.auth.models import User
# Create your models here.


METHOD = [(1,'POST'),(2, 'GET'),(3, 'DELETE'),(4, 'HEAD'),(5, 'OPTIONS'),(6, 'PUT')]
DELETE = [(1, "未删除"), (0, '已删除')]

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="项目名称",max_length=20,blank=False)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,default=None)
    userName = models.CharField(max_length=50)
    delete = models.IntegerField(choices=DELETE,default=1)
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class GlobalVariable(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20,verbose_name="全局变量表名称",blank=False)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,default=None)
    userName = models.CharField(max_length=50)
    delete = models.IntegerField(choices=DELETE, default=1)
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "全局变量"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class GlobalVariable_ext(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=20,verbose_name="键",blank=False)
    value = models.CharField(max_length=50,verbose_name="值",blank=True)
    globalId = models.ForeignKey(GlobalVariable,on_delete=models.DO_NOTHING,default=None)
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "全局变量表子表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.key

class TestCase(models.Model):
    TESTCASE_TYPE = [(1,'测试用例'),(2,'token')]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,verbose_name="测试用例名",blank=False)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,default=None)
    userName = models.CharField(max_length=50)
    testCaseType = models.IntegerField(choices=TESTCASE_TYPE,blank=False)
    delete = models.IntegerField(choices=DELETE, default=1)
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "测试用例"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class TestCaseSep(models.Model):


    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,verbose_name="测试用例步骤名",blank=False)
    url = models.URLField(max_length=100,verbose_name="链接",blank=False)
    method = models.IntegerField(choices=METHOD,default=2)
    headers = models.CharField(max_length=200,blank=True)
    token = models.IntegerField(verbose_name="token名",default=None)
    findVariable = models.CharField(max_length=50,blank=True)
    nameVariable = models.CharField(max_length=50,blank=True)
    expectResult = models.CharField(max_length=100,blank=True)
    maxTime = models.IntegerField(default=0)
    waitTime = models.IntegerField(default=0)
    index = models.IntegerField(default=0,blank=False)
    TestCaseId = models.ForeignKey(TestCase,on_delete=models.DO_NOTHING)
    paramsd = models.CharField(max_length=500,blank=True,default=None)
    datad = models.CharField(max_length=500,blank=True,default=None)
    jsond = models.CharField(max_length=500,blank=True,default=None)
    filesd = models.CharField(max_length=500,blank=True,default=None)

    class Meta:
        verbose_name = "测试用例步骤"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class TestCaseResultTotal(models.Model):
    id = models.AutoField(primary_key=True)
    projectName = models.CharField(max_length=50)
    passNums = models.IntegerField(default=0)
    failNums = models.IntegerField(default=0)
    errNums = models.IntegerField(default=0)
    createTime = models.DateTimeField(auto_now_add=True)
    times = models.FloatField(verbose_name="运行时间",max_length=20,default=0.00)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    userName = models.CharField(max_length=50)

    class Meta:
        verbose_name = "结果统计表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id

class TestCaseResult(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="测试用例名",blank=False,max_length=20)
    passNums = models.IntegerField(default=0)
    failNums = models.IntegerField(default=0)
    errNums = models.IntegerField(default=0)
    times = models.FloatField(max_length=20,default=0.00)
    Total_Id = models.ForeignKey(TestCaseResultTotal,on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "结果表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id

class TestCaseResult_ext(models.Model):
    RESULT = [(1,'PASS'),(2,'FAIL'),(3,'ERROR')]
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="测试用例步骤名",blank=False,max_length=20)
    url = models.URLField(max_length=100, verbose_name="链接", blank=False)
    method = models.IntegerField(choices=METHOD, default=2)
    headers = models.CharField(max_length=200, blank=True)
    paramsd = models.CharField(max_length=500,blank=True,default=None)
    datad = models.CharField(max_length=500,blank=True,default=None)
    jsond = models.CharField(max_length=500,blank=True,default=None)
    filesd = models.CharField(max_length=500,blank=True,default=None)
    response = models.CharField(max_length=1000,blank=True)
    code = models.IntegerField()
    result = models.IntegerField(choices=RESULT,default=1)
    testResult_id = models.ForeignKey(TestCaseResult,on_delete=models.DO_NOTHING)
    createTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "结果副表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id

class Project_TestCase(models.Model):
    id = models.AutoField(primary_key=True)
    projectId = models.ForeignKey(Project,on_delete=models.DO_NOTHING)
    testId = models.ForeignKey(TestCase,on_delete=models.DO_NOTHING)
    createTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "项目测试用例关联表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id
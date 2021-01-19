#coding:utf-8

import os
import shutil
import time
import zipfile,threading
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect

# Create your views here.
from APITest.Run import getRun
from django.utils.encoding import escape_uri_path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  #oneWeb
FBASE_DIR = os.path.abspath(os.path.dirname(os.getcwd()))  #git


lock = threading.Lock()

def zip_files(dir_path, zip_path,isDel=False):
    """
    :param dir_path: 需要压缩的文件目录
    :param zip_path: 压缩后的目录
    :return:
    """

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as f:
        for root, _, file_names in os.walk(dir_path):
            for filename in file_names:
                f.write(os.path.join(root, filename), filename)
                if isDel:
                    os.remove(os.path.join(root, filename))

def checkReport():
    try:
        reportPath =  BASE_DIR+"/APITest/report"
        fileSize = 0
        for root, dirs, files in os.walk(reportPath, topdown=False):
            for file in files:
                fileSize += os.path.getsize(os.path.join(root, file))
        if fileSize >= 1024 * 1024 * 100:
            zip_files(reportPath,BASE_DIR+"APITest/ZIP/" + str(int(time.time())) + '.zip', isDel=True)
    except Exception as e:
        print("检测报告文件夹大小是否超过10MB失败："+str(e))

def delFiles(fpath):
    try:
        if not os.path.isdir(fpath):
            print("请确认输入的是正确的路径！")
        else:
            dataList = os.listdir(fpath)
            for i in dataList:
                f = os.path.join(fpath,i)
                if os.path.isdir(f):
                    os.rmdir(f)
                elif os.path.isfile(f):
                    os.remove(f)
                else:
                    print(str(f)+'无法识别文件！')
    except Exception as e:
        print('删除文件失败： '+str(e))

def mycopyfile(srcfile,dstpath):                       # 移动函数
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(srcfile)             # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        fileList = os.listdir(dstpath)
        p = fname.split('.')[0]
        typ = fname.split('.')[-1]
        k = 1
        while fname in fileList:
            fname = p + '(' + str(k) + ').' + typ
            k += 1
        shutil.copy(srcfile, dstpath + fname)          # 移动文件
        print ("move %s -> %s"%(srcfile, dstpath + fname))

def getCodeFile(request):
    try:
        if request.method == 'POST':
            myFile = request.FILES.get('code_file', None)
            if not myFile:
                return redirect("/upload/")  # home page should with error
            fileList = os.listdir(BASE_DIR+"/APITest/code")
            fileName = myFile.name
            p = myFile.name.split('.')[0]
            typ = myFile.name.split('.')[-1]
            k = 1
            while fileName in fileList:
                fileName = p + '(' + str(k) + ').' + typ
                k += 1
            destination = open(
                os.path.join(BASE_DIR+"/APITest/code", fileName), 'wb+')

            for chunk in myFile.chunks():
                destination.write(chunk)
            destination.close()
            # name = fileName
            # mycopyfile(os.path.join(BASE_DIR+"\report", name),'D:/GIT/Test/APITest/code/')
            # renameFile('D:/GIT/Test/APITest/code/'+name,p)

            return redirect('/upload/')

        else:
            return redirect('/upload/')
    except Exception as e:
        print("处理文件失败："+str(e))


def upload(request):
    if request.method == "POST":
        while True:
            try:
                print(os.getpid())
                myFile = request.FILES.get('upload_file', None)
                if not myFile:
                    return redirect("/upload/")  # home page should with error
                fileList = os.listdir(BASE_DIR+"/APITest/TestData")
                fileName = myFile.name
                p = myFile.name.split('.')[0]
                typ = myFile.name.split('.')[-1]
                k = 1
                while fileName in fileList:
                    fileName = p+'('+str(k)+').'+typ
                    k+=1
                destination = open(
                    os.path.join(BASE_DIR+"/APITest/TestData", fileName), 'wb+')

                for chunk in myFile.chunks():
                    destination.write(chunk)
                destination.close()
                lock.acquire()
                #启动程序
                end = getRun(fileName)
                if end == 1:
                    result = '启动成功！'
                else:
                    result = '启动失败！'
                with open(BASE_DIR + '/APITest/log/logging.log', 'r') as f:
                    log = f.readlines()
                    f.close()

                file = BASE_DIR + "/APITest/code"
                listData = os.listdir(file)
                mycopyfile(BASE_DIR + '/APITest/log/logging.log', BASE_DIR + "/APITest/LOGZIP/")

                with open(BASE_DIR + '/APITest/log/logging.log', 'w') as f:
                    f.close()
                checkReport()

                content = {'result': result, 'log': log, 'codeFile': listData,'fileName':fileName}
                time.sleep(2)
                lock.release()
                return render(request,'result.html',content)
            except Exception as e:
                print("错误或等待中。。 " + str(e))

    else:
        return redirect("/upload/")

def getMkdir(request):


    listData = os.listdir(BASE_DIR+'/APITest/TestData')
    fileCodeList = os.listdir(BASE_DIR+'/APITest/code')

    context = {
        "MkdirData":listData,'codeFile': fileCodeList
    }
    return render(request,'upload.html',context)


def download_template(request):
    resultFile = open(BASE_DIR + "/APITest/模板.xlsx", 'rb')

    response = FileResponse(resultFile)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = "attachment;filename*=utf-8''{}".format(escape_uri_path("demo.xlsx"))
    return response

def download_user(request):
    resultFile = open(BASE_DIR + "/APITest/接口自动化操作手册.docx", 'rb')

    response = FileResponse(resultFile)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = "attachment;filename*=utf-8''{}".format(escape_uri_path("接口自动化使用手册.docx"))

    return response

def download_report(request):
    fileName = request.GET.get('filename')
    resultFile = open(BASE_DIR + "/APITest/TestData/"+fileName, 'rb')

    response = FileResponse(resultFile)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = "attachment;filename*=utf-8''{}".format(escape_uri_path(fileName))

    return response



def download_code(request):
    filename = request.GET.get('fn')

    resultFile = open(BASE_DIR + "/APITest/code/"+filename, 'rb')
    response = FileResponse(resultFile)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = "attachment;filename*=utf-8''{}".format(escape_uri_path(filename))

    return response

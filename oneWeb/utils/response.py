#coding:utf-8

from rest_framework.response import Response
from utils.Base64Code import CodeBase64
import json
from rest_framework import viewsets,status
from collections import OrderedDict
from rest_framework.utils.serializer_helpers import ReturnList
from django.db.models.query import QuerySet

class MyModelViewSet(viewsets.ModelViewSet):


    def create(self, request, *args, **kwargs):
        if len(self.authentication_classes) != 0:
            userInfo = getUser(request)
            if not userInfo:
                return APIResponse(statu=500,msg='fail',results='您暂未登陆，请重新登陆！')
            result = request.data.copy()
            result['user'] = userInfo['user_id']
            result['userName'] = userInfo['username']
        else:
            result = request.data
        serializer = self.get_serializer(data=result)

        is_valid = serializer.is_valid(raise_exception=False)
        if not is_valid:
            return APIResponse(statu=500,msg='fail',results=serializer.errors,status=status.HTTP_200_OK)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        #return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return APIResponse(statu=200,msg='success',results=serializer.data,status=status.HTTP_200_OK,headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if len(self.authentication_classes) != 0:
            userInfo = getUser(request)
            if not userInfo:
                return APIResponse(statu=500, msg='fail', results='您暂未登陆，请重新登陆！')
            try:
                queryset = queryset.filter(user=userInfo['user_id'])
            except Exception as e:
                pass
        total = len(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data  = serializer.data
            data = self.delFilter(data)
            #return self.get_paginated_response(serializer.data)
            return APIResponse(statu=200,msg='success',results=data,total=total)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        data = self.delFilter(data)
        #return Response(serializer.data)
        return APIResponse(statu=200,msg='success',results=data,total=total)


    def delFilter(self,data):
        if isinstance(data,dict) or isinstance(data,OrderedDict):
            if 'user' in list(data.keys()):
                del data['user']
            if 'userName' in list(data.keys()):
                del data['userName']
            if 'delete' in list(data.keys()):
                del data['delete']
            return data
        elif isinstance(data,ReturnList):
            for i in data:
                if 'user' in list(i.keys()):
                    del i['user']
                if 'userName' in list(i.keys()):
                    del i['userName']
                if 'delete' in list(i.keys()):
                    del i['delete']
            return data
        else:
            return data

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if len(self.authentication_classes) != 0:
            userInfo = getUser(request)
            if not userInfo:
                return APIResponse(statu=500, msg='fail', results='您暂未登陆，请重新登陆！')
            if serializer.data['user'] != userInfo['user_id']:
                return APIResponse(statu=200,msg='success',results=[])
        data = self.delFilter(serializer.data)
        #return Response(serializer.data)
        return APIResponse(statu=200,msg='success',results=data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        is_valid = serializer.is_valid(raise_exception=False)
        if not is_valid:
            return APIResponse(statu=500, msg='fail', results=serializer.errors, status=status.HTTP_200_OK)
        if len(self.authentication_classes) != 0:
            userInfo = getUser(request)
            if not userInfo:
                return APIResponse(statu=500, msg='fail', results='您暂未登陆，请重新登陆！')
            if serializer.data['user'] != userInfo['user_id']:
                return APIResponse(statu=500, msg='fail', results='您无权限修改！')
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        #return Response(serializer.data)
        return APIResponse(statu=200,msg='success',results=serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if len(self.authentication_classes) != 0:
            userInfo = getUser(request)
            if not userInfo:
                return APIResponse(statu=500, msg='fail', results='您暂未登陆，请重新登陆！')
            if serializer.data['user'] != userInfo['user_id']:
                return APIResponse(statu=500, msg='fail', results='您无权限修改！')
        data = serializer.data
        data['delete'] = 0
        serializer = self.get_serializer(instance,data=data)
        is_valid = serializer.is_valid(raise_exception=False)
        if not is_valid:
            return APIResponse(statu=500, msg='fail', results=serializer.errors, status=status.HTTP_200_OK)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        # return Response(serializer.data)
        return APIResponse(statu=200, msg='success', results=[])




class APIResponse(Response):
    def __init__(self,statu,msg,results=None,headers=None,status=None,**kwargs):
        data = {
            'status':statu,
            'msg':msg,
        }
        if results:
            data['results'] = results
        data.update(kwargs)
        super().__init__(data=data,headers=headers,status=status)


def getUser(request):
    try:
        token = request.META.get('HTTP_SUPER_TOKEN'.upper())
        tokenData = token.split('.')[1]
        userInfo = CodeBase64.decodeBase64(tokenData)
        userInfo = json.loads(userInfo)
        return {'user_id':userInfo['user_id'],'username':userInfo['username'],'email':userInfo['email']}
    except Exception as e:
        print("获取User信息失败，token无效！error:"+str(e))


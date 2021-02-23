#coding:utf-8
from rest_framework.pagination import PageNumberPagination


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'current'    #页数
    page_size_query_param = 'pageSize'  #一页大小
    max_page_size = 10000


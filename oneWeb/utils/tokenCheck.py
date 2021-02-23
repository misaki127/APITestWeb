#coding:utf-8
from functools import wraps

import jwt
from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication

class JWTAuthentication(BaseJSONWebTokenAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_SUPER_TOKEN'.upper())
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise AuthenticationFailed("登陆已过期,请重新登陆！")
        except jwt.DecodeError:
            raise AuthenticationFailed('暂未登陆，请重新登陆！')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("token不合法,请重新登陆！")
        user = self.authenticate_credentials(payload)
        return (user,token)




#coding:utf-8
import base64

class CodeBase64():
    #加密
    @staticmethod
    def encodeBase64(data):
        if isinstance(data,bytes):
            pass
        elif isinstance(data,str):
            data = base64.b64encode(data.encode())
        else:
            data = base64.b64encode(str(data).encode())
        return data.decode('utf-8')
    #解码
    @staticmethod
    def decodeBase64(data):
        if isinstance(data,str):
            data = bytes(data,'utf-8')
        missing_padding = len(data) % 4
        if missing_padding != 0:
            data += b'=' * (4-missing_padding)
        return base64.b64decode(data).decode('utf-8')

# -*- coding: utf-8 -*-
import random
import hmac
import base64
import hashlib

class AipBase(object):
    """
        AipBase
    """

    def __init__(self, appId, secretId, secretKey):
        """
            AipBase(appId,secretId,secretKey)
        """
        self._appID = appId
        self._secretId = secretId.strip()
        self._secretKey = secretKey.strip()
        self.__version = '1.0.0'

    def getVersion(self):
        return self.__version
    # 生成随机字符串
    def getrandom(self,length):
        nonce = ''
        for i in range(length):
            number = random.randint(1, 9)
            nonce = nonce + str(number)
        return int(nonce)

    # 字典排序算法
    def sordict(self,dict):
        after = sorted(zip(dict.keys(), dict.values()))
        return after

    # 算法参考地址
    # http://outofmemory.cn/code-snippet/33173/python-hmac-sha1
    def encrypt(self,signature1, secretkey):
        signature = bytes(signature1, encoding='utf-8')
        secretkey = bytes(secretkey, encoding='utf-8')
        # 这里python跟其他语言的写法不太一样。密钥在第一位，第二位才是要加密的。而且是bytes类型加密
        my_sign = hmac.new(secretkey, signature, hashlib.sha1).digest()
        my_sign = base64.b64encode(my_sign)
        return my_sign

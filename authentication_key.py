# coding=utf-8
import time
import requests
from config import *
import urllib.parse


# 官方文档地址：
# https://cloud.tencent.com/document/product/441/17366
# https://cloud.tencent.com/document/product/441/6201
def keygen(app_id, secretid, secretkey, projectid =0, engine_model_type="16k_0",
           callback_url="接受结果的回调url", res_text_format=0, source_type=1 ):
    """
    :param app_id: 在控制台“云API密钥”获得
    :param secretid: 在控制台“云API密钥”获得
    :param secretkey: 在控制台“云API密钥”获得
    :param projectid:  项目id, 默认0为默认项目
    :param engine_model_type: 采样率
    :param callback_url: 回调url
    :param res_text_format:
    :param source_type:
    :return: 加密后的签名，appid
    """
    timestamp = int(time.time()) # 当前时间的时间戳
    expired= timestamp +10000 # 签名有效期
    nonce = getrandom(6)                    # 随机正整数。用户需自行生成，最长 10 位
    app_id= app_id                      # 1256603936
    projectid = 0
    secretkey = secretkey
    secretid = secretid
    keydict ={
            "projectid": projectid,
            "sub_service_type": 0,
            "engine_model_type": engine_model_type,
            # 语音 URL，公网可下载。当 source_type 值为 0 时须填写该字段，为 1 时不填；URL 的长度大于 0，小于 2048
            # "url": "http://test.qq.com/rec_callback",
            "res_text_format": 0,
            "res_type": 1,
            "callback_url": "http://qa6iyt.natappfree.cc/test",
            "source_type": source_type,
            "secretid": secretid,
            "timestamp": timestamp,
            "expired": expired,
            "nonce": nonce,
        }
    # 字典排序后的字典
    sortkeydict = sordict(keydict)
    # 签名字符串拼接
    afterstr=''
    for i in sortkeydict:
        afterstr=afterstr+str(i[0])+'='+str(i[1])+'&'
    keystr = 'POSTaai.qcloud.com/asr/v1/'+str(app_id)+'?'
    signature1=(keystr+afterstr[:-1])
    print('拼接后的字符串', signature1)
    # 加密处理后，得到签名字符串
    # 签名字符可以保存，下次直接使用。
    signature_str = encrypt(signature1, secretkey)
    # 返回签名
    return signature_str,app_id,sortkeydict


# 语音识别接口访问，上传本地文件。url形式的上传可以参考官方文档。
def request2getjob_id(signature_str, app_id, filepath, sortkeydict):
    """

    :param signature_str: j加密后的签名
    :param app_id:   appid ,在控制台“云API密钥”获得
    :param filepath:  本地音频文件路径
    :param sortkeydict: 访问语音API需要的参数列表，已经过字典排序
    :return: job_id 任务id，用于获取语音结果。
    """
    print('签名字符',urllib.parse.quote(signature_str))
    body = ''
    with open(filepath, 'rb') as f:
        body = f.read()
    header={
        "Host": "aai.qcloud.com",
        "Content-Type": "application/octet-stream",
        "Authorization": signature_str,
        "Content-Length": str(len(body)),
    }

    url="http://aai.qcloud.com/asr/v1/"+str(app_id)+'?'+ urllib.parse.urlencode(sortkeydict)
    print(url)
    response=requests.post(url, data=body, headers=header)
    if response.status_code == 200 :
        print("上传识别音频文件成功")
        result=eval(str(response.content))
        # 任务ID
        job_id=result.get("requestid")
        return job_id
    else:
        print("失败")
        # 根据返回的code去腾讯的文档中心来查看是哪一步出错了
        # https://cloud.tencent.com/document/product/441/6201
        print(response.content)
        return 0
    return 0


#283569753
def response4job_id(job_id):
    # 回调接口上上面的方法中已经定义。可以用Flask+内网穿透来搭建一个接受回调的服务器。
    # 可以参考我的另一篇，没有的话，那就是我懒还没写。
    pass



if __name__ == "__main__":
    signature_str, app_id,sortkeydict=keygen("your","your","your")
    request2getjob_id(signature_str,app_id,r'F:/10.mp3',sortkeydict)
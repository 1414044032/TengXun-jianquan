# 腾讯鉴权实现整个流程
## 例子为语音识别接口的实现：
----
### TXspeek.py为主文件，其中的class AipSpeech继承自test中base.pyAipBase。
### AipSpeech实现了“拼接参数”，“生成签名”,"语音识别接口访问"。
### 实例化 AipSpeech(yourappid,"yourid","yourkey") 需要三个参数，对应你的腾讯云给的。
### 上传成功后，会返回响应信息，并且，识别成功后，会把识别后的内容回调给回调地址写的接口中。
----
## 使用方法：
### 填充参数即可：

     回调地址 (接受响应的外网地址)
    call_url = "http://ksp2tc.natappfree.cc/test"
     实例化类，填写腾讯云提供的参数
    speech = AipSpeech("yourappid","yourid","yourkey")
     生成参数列表
    sortkeydict = speech.sortparms(call_url)
     生成签名
    signature_str = speech.keygen(sortkeydict)
     调用语音识别方法
     speech.request2getjob_id(signature_str, speech._appID, r"F:\08.mp3", sortkeydict) # 填写本地语音地址'

#导入所有的库
import win32com.client
import time
import sys
import pyaudio
from playsound import playsound
from aip import AipSpeech
import wave
import requests
import json
import random
from aip import AipSpeech
import urllib.request
import hashlib
import os
#百度API
########################################下面必填########################################################
APP_ID,API__KEY,SECRET_KEY,Bot_ID,skill_ID = '','','','','1017780'
speaker = win32com.client.Dispatch("SAPI.SpVoice")

#读取主要的参数，其实我也忘了是干啥的
client = AipSpeech(APP_ID,API__KEY,SECRET_KEY)

#读取音频
def read_file(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

#录音
def audio(RECORD_SECONDS,ty):#录音
    """PyAudio example: Record a few seconds of audio and save to a WAVE file."""
    CHUNK = 2048
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    WAVE_OUTPUT_FILENAME = "audio.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    if ty == 2:
        print("收到，请讲")
    else:
        print(1)

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    if ty ==2:
        print("停止")
    else:
        print(2)
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

#获取试别内容
def gettxt():
    return client.asr(read_file('audio.wav'), 'pcm', 16000, {
        'dev_pid': 1536,
    })


#调用图灵接口，emmmmmm，要钱，就没弄
def tuling_reply(url, apikey, msg):
    data = {  # 这个是在帮助手册上直接复制过来的，"url"=="https://www.kancloud.cn/turing/www-tuling123-com/718227"
        # """与reqType在同一级的参数有：{
        # reqType : 输入类型
        # perception : 输入信息
        # userInfo : 用户参数"""
        "reqType": 0,
        # '''# reqType为int类型，可以为空，
        # 输入类型:{
        # 0:文本(默认)
        # 1:图片
        # 2:音频
        # }'''
        "perception": {  # perception为用户输入信息，不允许为空
            # """
            # perception参数中的参数有：{
            # inputText : 文本信息
            # inputImage : 图片信息
            # inputMedia : 音频信息
            # selfInfo : 客户端属性
            # }
            # 注意：输入参数必须包含inputText或inputImage或inputMedia，可以是其中的任何一个\
            # 也可以是全部！
            # """
            # 用户输入文文信息
            "inputText": {  # inputText文本信息
                "text": msg
            },
            # 用户输入图片url
            "inputImage": {  # 图片信息，后跟参数信息为url地址，string类型
                "url": "https://cn.bing.com/images/"
            },
            # 用户输入音频地址信息
            "inputMedia": {  # 音频信息，后跟参数信息为url地址，string类型
                "url": "https://www.1ting.com/"
            },
            # 客户端属性信息
            "selfInfo": {  # location 为selfInfo的参数信息，
                "location": {  # 地理位置信息
                    "city": "深圳",  # 所在城市，不允许为空
                    "province": "广东省",  # 所在省份，允许为空
                    "street": "南山"  # 所在街道，允许为空
                }
            },
        },
        "userInfo": {  # userInfo用户参数，不允许为空
            # """
            # "userInfo包含的参数":{
            # "apiKey" : {
            #     "类型" : "String",
            #     "是否必须" : "Y ",
            #     "取值范围" : "32位",
            #     "说明" : "机器人标识"
            #     }
            # "userId" : {
            #     "类型" : "String",
            #     "是否必须" : "Y ",
            #     "取值范围" : "长度小于等于32位",
            #     "说明" : "用户唯一标识"
            #     }
            # "gropId" : {
            #     "类型" : "String",
            #     "是否必须" : "N ",
            #     "取值范围" : "长度小于等于64位",
            #     "说明" : "群聊唯一标识"
            #     }
            # "userIdName" : {
            #     "类型" : "String",
            #     "是否必须" : "N ",
            #     "取值范围" : "长度小于等于64位",
            #     "说明" : "群内用户昵称"
            #     }
            # }
            # """
            "apiKey": "20746060dfe1427a8eedbbe344100f35",  # 你注册的apikey,机器人标识,32位
            "userId": "anystring168"  # 随便填，用户的唯一标识，长度小于等于32位
        }
    }
    headers = {'content-type': 'application/json'}  # 必须是json
    r = requests.post(url, headers=headers, data=json.dumps(data))
    return r.json()
#收到图灵的回复
def reply(msg):
    apikey = '20746060dfe1427a8eedbbe344100f35'  # 填入机器人的apikey
    url = 'http://openapi.tuling123.com/openapi/api/v2'  # 图灵机器人的v2.0接口地址
    # print(json.dumps(tuling_reply.data))
    msg = msg.strip()
    reply = tuling_reply(url, apikey, msg)
    return reply["results"][0]["values"]["text"]# 可以直接打印reply


#获取百度的token，反正必须要。
def gettoken():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+API__KEY+'&client_secret='+SECRET_KEY
    response = requests.get(host)
    response = response.json()
    token = str(response['access_token'])
    return token
#收到百度的回复
def baidu_reply(msg):
    access_token = gettoken()#获取token
    url = 'https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=' + access_token#组装url
    #下面敲重点
    post_data = {"bot_id":skill_ID,"log_id":"UNITTEST_10000","version":"2.0","service_id":Bot_ID,"session_id":" ","request":{"query":msg,"user_id":"88888"},"dialog_state":{"contexts":{"SYS_REMEMBERED_SKILLS":["1057"]}}}
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    post_data = json.dumps(post_data)#官网的代码有错误，竟然无法运行。。。。所以我试了几十分钟，找到了办法解决，做成字典，然后转为json
    response = requests.post(url, data =post_data, headers=headers)#发送请求
    response=response.json()#返回json
    return response['result']['response_list'][0]['action_list'][random.randint(0,len(response['result']['response_list'][0]['action_list']))]['say']#这里最重要，我搞了好久
#百度文字转语音
def readtxt(txt):
    result = client.synthesis(txt, 'zh', 1, {
        'vol': 5,'per': 4
    })

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('auido.mp3', 'wb') as f:
            f.write(result)
    playsound('auido.mp3')

#小i开放平台（一个免费的平台，自认为超级好用）
class xiaoi_bot(object):
    def __init__(self, appKey, appSecret):
        appKey = appKey
        appSecret = appSecret
        HA1 = hashlib.sha1(
            ':'.join([appKey, "xiaoi.com", appSecret]).encode("utf8")).hexdigest()
        HA2 = hashlib.sha1(u"GET:/ask.do".encode("utf8")).hexdigest()
        nonce = self.getNonce()  # ':'.join([HA1, nonce, HA2]).encode("utf8")
        sig = hashlib.sha1(
            ':'.join([HA1, nonce, HA2]).encode("utf8")).hexdigest()

        self.headers = {
            "X-Auth": "app_key=\"{0}\",nonce=\"{1}\",signature=\"{2}\"".format(
                appKey, nonce, sig)
        }

    def GetResponse(self, question, userId='test'):
        post_data = {
            "question": question,
            "userId": userId,
            "type": "0",
            "platform": "web"
        }
        post_data = urllib.parse.urlencode(post_data)
        url = "http://robot.open.xiaoi.com/ask.do?"+post_data
        request = urllib.request.Request(url, None, self.headers)
        request.add_header('Content-Type', 'text/html; charset=UTF-8')
        response = urllib.request.urlopen(request)
        return str(response.read(), 'utf8') #response.read()

    def getNonce(self):
        strs = ''
        for i in range(18):
            strs += (str(random.randint(0, 15)))
        return strs

#百度运行的对话
def run_baidu():
    while True:
        audio(2,1)
        dicts = gettxt()
        print(dicts)
        try:
            get = dicts['result']
            get = str(get)
            if '小天' in get:
                audio(3.5,2)
                dicts = gettxt()
                get = dicts['result']
                get = str(get)
                if get == 'None':

                    print('对不起，我不知道你在说什么')
                    continue
                else:
                    msg = baidu_reply(get)
                    print(msg)
                    readtxt(msg)


            elif '退出程序' in get:
                break
            else:
                continue
        except:
            continue

#小艾的对话
def run_xiaoi():
    bot = xiaoi_bot("open1_IIqFAd3ZBgd6", "pOWHjEblULVr4pSQMjiS")
    while True:
        audio(2, 1)
        dicts = gettxt()
        
        try:
            get = dicts['result']
            get = str(get)
            if '小天' in get:
                audio(3.5, 2)
                dicts = gettxt()
                get = dicts['result']
                get = str(get)
                if get == 'None':

                    print('对不起，我不知道你在说什么')
                    continue
                else:
                    msg = bot.GetResponse(get, "1")
                    print(msg)
                    readtxt(msg)




            elif '退出程序' in get:
                break
            else:
                continue
        except:
            continue
run_xiaoi()

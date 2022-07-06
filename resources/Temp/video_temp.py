import json
from aip import AipSpeech
from urllib import request,parse
# 申请百度语音识别
APP_ID = '25749667'
API_KEY = 'liENvMOUcb7OdpN4y8fsXNrT'
SECRET_KEY = 'bV6D7dcS6c2lESjOPFax4hYrex4UEeDV'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
Url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id="+API_KEY+"&client_secret="+SECRET_KEY

def get_token():
    try:
        resp = request.urlopen(Url)
        result = json.loads(resp.read().decode('utf-8'))
        # 打印access_token
        print("access_token:",result['access_token'])
        return result['access_token']
    except request.URLError as err:
        print('token http response http code : ' + str(err.code))

def speak():
    # 1、获取 access_token
    token = get_token()
    # 2、打开需要识别的语音文件
    speech_data = []
    with open("test.wav", 'rb') as speech_file:
        speech_data = speech_file.read()
    length = len(speech_data)
    if length == 0:
        print('file 01.wav length read 0 bytes')

    # 3、设置Url里的参数
    params = {'cuid': "12345678python", # 用户唯一标识，用来区分用户，长度为60字符以内。
              'token': token,           # 我们获取到的 Access Token
              'dev_pid': 1537 }         # 1537 表示识别普通话
    # 将参数编码
    params_query = parse.urlencode(params)
    # 拼接成一个我们需要的完整的完整的url
    Url = 'http://vop.baidu.com/server_api' + "?" + params_query

    # 4、设置请求头
    headers = {
        'Content-Type': 'audio/wav; rate=16000',    # 采样率和文件格式
        'Content-Length': length
    }

    # 5、发送请求，音频数据直接放在body中
    # 构建Request对象
    req = request.Request(Url, speech_data, headers)
    # 发送请求
    res_f = request.urlopen(req)
    result = json.loads(res_f.read().decode('utf-8'))
    print(result)
    print("识别结果:",result['result'][0])
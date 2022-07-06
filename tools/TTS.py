from aip import AipSpeech
import pyaudio
import wave

# 申请百度语音识别
APP_ID = '25749667'
API_KEY = 'liENvMOUcb7OdpN4y8fsXNrT'
SECRET_KEY = 'bV6D7dcS6c2lESjOPFax4hYrex4UEeDV'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
# 文字转换为语音
def text_to_audio(text):
    file = 'test2.wav'
    synth = client.synthesis(text, 'zh', 1, {'vol': 5, 'spd': 6, 'per': 3})
    f = open(file, 'wb')
    f.write(synth)
    f.close()
    return file

# Python播放音频文件
def play_audio(file):
    p = pyaudio.PyAudio()
    wf = wave.open(file, 'rb')
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(1024)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(1024)
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()

text = '今天下雨，明天天晴'
tp=text_to_audio(text)
play_audio(tp)
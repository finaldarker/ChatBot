import threading
import time
import jieba
import tkinter as tk
import pyttsx3
from tkinter import END, WORD
from PIL import Image, ImageTk, ImageSequence
from model.encoder_decoder import word_filter, word_wise, evaluate, encoder, decoder, voc, GreedySearchDecoder
from aip import AipSpeech
import pyaudio
import wave

# 申请百度语音识别
APP_ID = '25749667'
API_KEY = 'liENvMOUcb7OdpN4y8fsXNrT'
SECRET_KEY = 'bV6D7dcS6c2lESjOPFax4hYrex4UEeDV'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

chatbot_name='鲸梦QvQ'
picture_path='../resources/BG/'
save_path='../resources/messages/'
pet_path='../resources/pets/'
video_path='../resources/video/test.wav'
# 将识别功能封装成函数
def recognize(file):
    data = open(file, 'rb').read()
    result = client.asr(data, 'wav', 16000, {'dev_pid': 1537})
    return result['result'][0]


# Python录音
def get_audio(sec):
    # 创建对象
    p = pyaudio.PyAudio()
    # 创建流:采样位，声道数，采样频率，缓冲区大小，input=True
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    # 创建式打开音频文件
    wf = wave.open(video_path, 'wb')
    # 设置音频文件的属性:声道数，采样位，采样频率
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    print('开始录音')
    for w in range(int(16000 * sec / 1024)):
        data = stream.read(1024)
        wf.writeframes(data)
    print('录音结束')
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()
    return video_path

def pick():
    while 1:
        im = Image.open(pet_path+'mouse.gif')
        # GIF图片流的迭代器
        iter = ImageSequence.Iterator(im)
        #frame就是gif的每一帧，转换一下格式就能显示了
        for frame in iter:
            pic=ImageTk.PhotoImage(frame)
            pet_bot.create_image((50,23), image=pic,anchor ='n')
            time.sleep(0.1)
            Chat.update_idletasks()  #刷新
            Chat.update()

def speak(chat_an):
    engine = pyttsx3.init()   # 初始化
    engine.setProperty('voice', "com.apple.speech.synthesis.voice.sin-ji")  #设置发音人
    #engine.setProperty('voice', "com.apple.speech.synthesis.voice.mei-jia")
    rate = engine.getProperty('rate')  # 改变语速  范围为0-200   默认值为200
    engine.setProperty('rate', rate-40)
    engine.setProperty('volume', 0.7)  # 设置音量  范围为0.0-1.0  默认值为1.0
    engine.say(chat_an)   # 预设要朗读的文本数据
    engine.runAndWait()   # 读出声音

#QA输出
def QAInput(talk_in):
    input_sentence=talk_in
    input_sentence = word_filter(jieba.cut(input_sentence) if word_wise else input_sentence)
    # 生成响应Evaluate sentence
    output_words = evaluate(encoder, decoder, searcher, voc, input_sentence)
    # 去掉EOS后面的内容
    chat_words = []
    for word in output_words:
        if word == 'EOS':
            break
        elif word != 'PAD':
            chat_words.append(word)
    talk_on=''.join(chat_words)
    return talk_on

def sendvideo():
    file = get_audio(6)
    temp=recognize(file)
    receive_message.insert(END, '我:' + temp+'\n')
    chat_answer=QAInput(temp)
    if chat_answer == '' or chat_answer == '哦了哦了哦了咱聊点别的吧':
        with open(save_path + 'unknown_messages.txt', 'a', encoding='utf-8') as ms:
            q = temp.strip()
            ms.write(q +'|a'+ '\n')
        receive_message.insert(END,'{}：'.format(chatbot_name) + '我还没学会回答这问题呢。'+'\n')
        speak('我还没学会回答这问题呢。')
    else:
        receive_message.insert(END,'{}：'.format(chatbot_name) + chat_answer+'\n')
        speak(chat_answer)
        # 把聊天内容保存用于下次分词
        with open(save_path + 'chat_messages.txt', 'a', encoding='utf-8') as ms:
            q = temp.strip()
            a = chat_answer.strip()
            ms.write(q + '|' + a + '\n')


Chat = tk.Tk()
# 进入eval模式，从而去掉dropout。
encoder.eval()
decoder.eval()
# 构造searcher对象
searcher = GreedySearchDecoder(encoder, decoder)
ws = Chat.winfo_screenwidth()
hs = Chat.winfo_screenheight()
 # 窗口设置
Chat.geometry("431x345+468+186")#界面尺寸+界面位置
Chat.resizable(width=False, height=False)  # False禁止为最大化
Chat.config(background="#ffffff")
Chat.title("ChatBot")
Chat.iconbitmap(picture_path + 'log.ico')
#chatbot一栏设置（左栏）
chatbot_list=tk.Frame(Chat, bg="#ffffff", cursor='xterm')
chatbot_list.pack(side='left',anchor="n")
#聊天对象u
chatbot_image = tk.PhotoImage(file=picture_path + 'head.png')
chatbot = tk.Label(chatbot_list, image=chatbot_image,bg='#ffffff', width=98, height=98)
chatbot.pack()
chatbot_text_image=tk.PhotoImage(file=picture_path + 'click.png')
chatbot_text=tk.Label(chatbot_list,image=chatbot_text_image,bg="#ffffff",width=98, height=118, font=('腾祥爱情体简', 15))
chatbot_text.pack()
pet_bot = tk.Canvas(chatbot_list, width=98, height=237, bg='#ffffff')
pet_bot.pack()
thrd_once=threading.Thread(target=pick)
thrd_once.start()
# chat一栏设置（右栏）
state=0
chat_list = tk.Frame(Chat, bg="#ffffff", cursor='xterm', width=98, height=98)
chat_list.pack(side='right')
# 聊天对象
title_lbl = tk.Label(chat_list, text=chatbot_name, bg="#ffffff", font=('腾祥爱情体简', 10))
title_lbl.pack(side='top', anchor="w")
# 接收消息
# 在聊天内容上方加一行 显示发送人及发送时间
content = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
receive_message= tk.Text(chat_list, height=11, width=37, font=('腾祥爱情体简', 12),wrap=WORD)
receive_message.insert(END, content)
receive_message.pack()
# 发送消息
send_message = tk.Button(chat_list, text='录音',height=5, width=37, font=('腾祥爱情体简', 12),command=sendvideo)
send_message.pack()
Chat.mainloop()
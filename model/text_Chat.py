import os
import threading
import time
import jieba
import tkinter as tk
import pyttsx3
import tkinter.filedialog
from tkinter import END, WORD
from PIL import Image, ImageTk, ImageSequence
from ChatBot.tools.image_handle import image_handle
from encoder_decoder import word_filter, word_wise, evaluate, encoder, decoder, voc, GreedySearchDecoder

chatbot_name='鲸梦QvQ'
picture_path='../resources/BG/'
save_path='../resources/messages/'
pet_path='../resources/pets/'

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

def FileOpen(event):
    head_file = tk.filedialog.askopenfilename(title='请选择一个文件',filetypes=[('PNG','png'), ('JPG','jpg'), ('GIF','gif')])
    image_handle(head_file)
    Chat.update()
    global img2
    img2=tk.PhotoImage(file=os.path.abspath(picture_path+'head_temp.png'))
    chatbot.config(image=img2)

def sendmessage():
    receive_message.insert(END, '我:' + send_message.get('0.0', END).strip('\n')+'\n')
    temp = send_message.get('0.0', END)
    input_sentence = send_message.get('0.0', END)
    global chat_answer
    chat_answer=QAInput(input_sentence)
    send_message.delete('0.0', END)
    if chat_answer == '哦了哦了哦了咱聊点别的吧' or chat_answer ==' ':
        receive_message.insert(END, '{}：'.format(chatbot_name) + '我还没学会回答这问题呢' + '\n')
        receive_message.see(END)
        with open(save_path + 'unknown_messages.txt', 'a', encoding='utf-8') as ms:
            q = temp.strip()
            ms.write(q +'|a'+ '\n')
    else:
        receive_message.insert(END,'{}：'.format(chatbot_name) + chat_answer+'\n')
        receive_message.see(END)
        # 把聊天内容保存用于下次分词
        with open(save_path + 'chat_messages.txt', 'a', encoding='utf-8') as ms:
            q = temp.strip()
            a = chat_answer.strip()
            ms.write(q + '|' + a + '\n')

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

def speak():
    engine = pyttsx3.init()   # 初始化
    engine.setProperty('voice', "com.apple.speech.synthesis.voice.sin-ji")  #设置发音人
    #engine.setProperty('voice', "com.apple.speech.synthesis.voice.mei-jia")
    rate = engine.getProperty('rate')  # 改变语速  范围为0-200   默认值为200
    engine.setProperty('rate', rate-40)
    engine.setProperty('volume', 0.7)  # 设置音量  范围为0.0-1.0  默认值为1.0
    engine.say(chat_answer)   # 预设要朗读的文本数据
    engine.runAndWait()   # 读出声音

def enter(event):
    thrd_once=threading.Thread(target=sendmessage)
    thrd_once.start()

#GUI设计
Chat = tk.Tk()
# 进入eval模式，从而去掉dropout。
img= tk.PhotoImage(file=picture_path + 'head.png')
encoder.eval()
decoder.eval()
searcher = GreedySearchDecoder(encoder, decoder)
 # 窗口设置
Chat.geometry("431x345+468+186")#界面尺寸+界面位置
Chat.resizable(width=False, height=False)  # False禁止为最大化
Chat.config(background="#ffffff")
Chat.title("ChatBot")
Chat.iconbitmap(picture_path + 'log.ico')
#chatbot一栏设置（左栏）
chatbot_list=tk.Frame(Chat, bg="#ffffff", cursor='xterm')
chatbot_list.pack(side='left',anchor="n")
#聊天对象
chatbot = tk.Label(chatbot_list, image=img,bg='#ffffff', width=98, height=98)
chatbot.pack()
chatbot.bind('<Button-1>',FileOpen)
chatbot_text_image=tk.PhotoImage(file=picture_path + 'click.png')
chatbot_text=tk.Label(chatbot_list,image=chatbot_text_image,bg="#ffffff",width=98, height=118, font=('腾祥爱情体简', 15))
chatbot_text.pack()
pet_bot = tk.Canvas(chatbot_list, width=98, height=237, bg='#ffffff')
pet_bot.pack()
thrd_once=threading.Thread(target=pick)
thrd_once.start()
# chat一栏设置（右栏）
chat_list = tk.Frame(Chat, bg="#ffffff", cursor='xterm', width=98, height=98)
chat_list.pack(side='right')
# 聊天对象
title_lbl = tk.Label(chat_list, text=chatbot_name, bg="#ffffff", font=('腾祥爱情体简', 10))
title_lbl.pack(side='top', anchor="w")
lbl = tk.Label(chat_list,bg="#ffffff")
lbl.pack(side='top')
# 接收消息
# 在聊天内容上方加一行 显示发送人及发送时间
scroll=tk.Scrollbar(lbl)
scroll.pack(side='right',fill=tk.Y)
receive_message= tk.Text(lbl, height=11, width=37, font=('腾祥爱情体简', 12),wrap=WORD,yscrollcommand = scroll.set)
content = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
receive_message.insert(END, content)
receive_message.pack(side='left')
scroll.config(command = receive_message.yview)
# 发送消息
send_message = tk.Text(chat_list, height=5, width=38, font=('腾祥爱情体简', 12))
send_message.pack()
send_message.bind('<Return>',enter)
# 发送按钮
btn = tk.Button(chat_list, text="发送", bg="white", font=('腾祥爱情体简', 10), cursor='crosshair',activebackground='grey',command=sendmessage)
btn.pack(side='right',padx=4)
speak=tk.Button(chat_list,text="转语音", bg="white", font=('腾祥爱情体简', 10), cursor='crosshair',activebackground='grey',command=speak)
speak.pack(side='left',padx=4)
Chat.mainloop()
os.replace(picture_path + 'head_temp.png',picture_path + 'head.png')


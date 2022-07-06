import random
import threading
import time
import tkinter as tk
from tkinter import END
from PIL import Image, ImageTk, ImageSequence
from encoder_decoder import corpus

chatbot_name='鲸梦QvQ'
chat_answer=''
picture_path='../resources/BG/'
save_path='../resources/messages/'
pet_path='../resources/pets/'
#corpus_path='ChatBot/resources/chat_corpus/鲸梦.csv'
def sendmessage():
    receive_message.insert(END, '我：' + send_message.get('0.0', END).strip('\n')+'\n')
    chat_answer = send_message.get('0.0', END)
    send_message.delete('0.0', END)
    receive_message.see(END)
    # 把聊天内容保存用于下次分词
    with open(save_path+'study_messages.txt','a',encoding='utf-8') as st_on:
        st_on.write(chat_question+'|'+chat_answer)
    study()

def study():
    global chat_question
    unknown=[]
    with open(save_path+'unknown_messages.txt', "r", encoding="utf-8") as f:
        lines = f.readlines()
        unknown=lines
        study_in=random.choice(unknown)
        study_on = ''.join(study_in.split())
        chat_question=study_on.strip('|a')
    with open(save_path+'unknown_messages.txt', "w", encoding="utf-8") as f_w:
        for line in lines:
            if study_in in line:
                continue
            else:f_w.write(line)
    receive_message.insert(END, '{}：'.format(chatbot_name) + chat_question + '\n')

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

def merge(study_input,study_output):
    with open(study_input, 'r', encoding='utf-8') as input, open(study_output, 'a',encoding='utf-8') as output:
        for index, line in enumerate(input):
            st_input=line.split('\n')
            st_input1=''.join(st_input)
            output.write(st_input1)
    with open(study_input, 'w', encoding='utf-8') as temp:
        temp.close()

def enter(event):
    thrd_once=threading.Thread(target=sendmessage)
    thrd_once.start()

#GUI设计
Chat = tk.Tk()
#窗口设置
Chat.geometry("431x345+468+186")
Chat.resizable(width=False, height=False)#False禁止为最大化
Chat.config(background="#ffffff")
Chat.title("ChatBot")
Chat.iconbitmap(picture_path+'log.ico')

#chatbot一栏设置（左栏）
chatbot_list=tk.Frame(Chat, bg="#ffffff", cursor='xterm')
chatbot_list.pack(side='left',anchor="n")
#聊天对象
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

#chat一栏设置（右栏）
chat_list = tk.Frame(Chat, bg="#ffffff", cursor='xterm',height=345, width=37)
chat_list.pack(side='right')
#聊天对象
title_lbl = tk.Label(chat_list, text=chatbot_name,bg="#ffffff", font=('腾祥爱情体简', 10))
title_lbl.pack(side='top',anchor="w")
#接收消息

receive_message = tk.Text(chat_list, height=11, width=37, font=('腾祥爱情体简', 12))
# 在聊天内容上方加一行 显示发送人及发送时间
content =time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
receive_message.insert(END, content+'\n')
study()
receive_message.pack()
#发送消息
send_message = tk.Text(chat_list, height=5, width=37, font=('腾祥爱情体简', 12))
send_message.pack()
send_message.bind('<Return>',enter)
#发送按钮
btn = tk.Button(chat_list, text="发送", bg="white", font=('腾祥爱情体简', 10), cursor='crosshair', activebackground='grey',
command=sendmessage)
btn.pack(side='right')
Chat.mainloop()
merge(save_path+'study_messages.txt',corpus)
# ChatBot
train_model.py为训练模型的脚本
encoder_decoder.py为模型的脚本文件
text_Chat.py为文本聊天界面
video_Chat.py为语音聊天界面
study_model.py为学习模型脚本，该脚本会在聊天过程中未知的问题进行收集，然后通过该脚本人为的告诉它正确的回答。然后在下次训练时就能学习了。
里面的工具是一些数据功能的工具，然后是一些小工具。
github中训练上传文件有限制，如需进行，在encoder_decoder.py文件中设置loadFilename =None，并把下面一样的loadFilename注释掉。下次读取模型把下面的注释放开，注释上面的代码。

import os
import re

chat_corpus_input = 'test_sample/test.txt'
#chat_corpus_input = 'xiaohuangji.conv'
chat_corpus_output = 'xiaohuangji.txt'
stopwords_path = '../chat_corpus/test_sample/China.txt'
#stopwords_path = '../resources/chat_corpus/Chinese_Names_Corpus（120W）.txt'
file_input_path = os.path.abspath('../resources/chat_corpus/{}'.format(chat_corpus_input))
file_output_path = os.path.abspath('../resources/chat_corpus/{}'.format(chat_corpus_output))


# 去重
def de_weight(file_input):
    temp = set()
    with open(file_input, 'r', encoding='utf-8') as inputs:
        for index, line in enumerate(inputs):
            line = inputs.readline()
            temp.add(line)
    with open(file_input, 'w', encoding='utf-8') as inputs:
        inputs.writelines(temp)

# 去人名
def data_to_noise(file_input, file_output, file_stop):
    with open(file_input, 'r', encoding='utf-8') as inputs, open(file_output, 'w', encoding='utf-8') as outputs, open(
            file_stop, 'r', encoding='utf-8') as names:
        name=names.readlines()
        words = inputs.readlines()
        print(words)


    '''
def data_to_noise(file_input, file_output, file_stop):
    name=[]
    words=[]
    counts=0.0
    with open(file_input, 'r', encoding='utf-8') as inputs, open(file_output, 'w', encoding='utf-8') as outputs, open(
            file_stop, 'r', encoding='utf-8') as names:
        for line in names.readlines():
            name.append(line.rstrip('\n'))
        for line in inputs.readlines():
            words.append(line.rstrip('\n'))
        for i in name:
            for j in words:
                counts=counts+1
                if counts%(500*len(name))==0:
                    print(str(counts/len(words)/len(name)*100)+'%')
                if i in j:
                    n=words.index(j)
                    words[n]=''
        for i in words:
            outputs.write(i+'\n')
    '''


# de_weight(file_input_path)
data_to_noise(file_input_path, file_output_path, stopwords_path)

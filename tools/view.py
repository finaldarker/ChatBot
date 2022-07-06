import jieba

#input_file = '../resources/chat_corpus/test_sample/test.txt'
#input_file = '../resources/chat_corpus/Chinese_Names_Corpus（120W）.txt'
input_file = '../resources/chat_corpus/xiaohuangji.conv'
stop_file = '../resources/chat_corpus/stopword.txt'
output_file = '../resources/segments/words.txt'
save_file = '../resources/segments/words.txt'
#save_file = '../resources/counts/words_counts.txt'


# 创建停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open(stop_file, encoding='UTF-8').readlines()]
    return stopwords


# 对句子进行中文分词
def seg_depart(sentence):
    # 对文档中的每一行进行中文分词
    sentence_depart = jieba.cut(sentence.strip())
    # 创建一个停用词列表
    stopwords = stopwordslist()
    # 输出结果为outstr
    outstr = ''
    # 去停用词
    tp = []
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t' and len(word) >= 2:
                tp.append(word)
                outstr += word
                outstr += " "
    return outstr, tp



# 给出文档路径
inputs = open(input_file, 'r', encoding='UTF-8')
outputs = open(output_file, 'w', encoding='UTF-8')

# 将输出结果写入ou.txt中
t=[]
for line in inputs:
    line_seg,s = seg_depart(line)
    t=t+s
    outputs.write(line_seg + '\n')
outputs.close()
inputs.close()
save=open(save_file, 'w', encoding='UTF-8')
for i in set(t):
    if len(i) == 3 or len(i) == 4:
        save.write(i+'\n')
save.close()
print("分词成功！！！")


def delete_name(input_file, output_file,save_file):
    with open(input_file, 'r', encoding='utf-8') as inputs, open(output_file, 'w', encoding='utf-8') as outputs, open(
            save_file, 'r', encoding='utf-8') as saves:
        save = saves.readlines()
        counts=0.0
        for index,line in enumerate(inputs):
            counts=counts+1
            if line in save:
                outputs.write(line)
            if counts%10000==0:
                print(str((counts/1145000)*100)+'%')

#delete_name(input_file, output_file,save_file)
def delete_to_names(input_file,save_file):
    with open(input_file, 'r', encoding='utf-8') as inputs,open(save_file, 'r', encoding='utf-8') as saves:
        name=saves.readlines()
        scores = 0.0
        for i in range(len(name)):
            name[i]=name[i].strip('\n')
        words=inputs.readlines()
        for i in range(len(words)):
            for j in range(len(name)):
                scores=scores+1
                if name[j] in words[i]:
                    words[i]=''
                if scores%500==0:
                    print(str((scores/len(words)/len(name))*100)+'%')
    with open(input_file, 'w', encoding='utf-8') as inputs:
        print(words)
        inputs.writelines(words)

delete_to_names(input_file,save_file)
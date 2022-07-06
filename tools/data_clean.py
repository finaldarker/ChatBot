input_file= '../resources/chat_corpus/鲸梦.csv'
output_file='../resources/Temp/qingyun_unknown.csv'
temp_file='../resources/Temp/temp.csv'

def remove_unknown(input_file,output_file,words):
    with open(input_file,'r',encoding='utf-8') as inputs,open(output_file,'a',encoding='utf-8') as outputs:
        tp=[]
        for index,line in enumerate(inputs):
            if words not in line:
                tp.append(line)
            else:outputs.write(line)
    with open(input_file,'w',encoding='utf-8') as outputs:
        for i in tp:
            outputs.write(i)

def replace_unknown(input_file,old_words,new_words):
    with open(input_file, 'r', encoding='utf-8') as inputs:
        tp=[]
        for index, line in enumerate(inputs):
            if old_words in line:
                t=line.replace(old_words,new_words)
                tp.append(t)
            else:tp.append(line)
    with open(input_file, 'w', encoding='utf-8') as outputs:
        for i in tp:
            outputs.write(i)

def remove_len(input_file,output_file):
    with open(input_file, 'r', encoding='utf-8') as inputs,open(output_file,'a',encoding='utf-8') as outputs:
        tp=[]
        for index, line in enumerate(inputs):
            if len(line)>30:
                outputs.write(line)
            else:tp.append(line)
    with open(input_file, 'w', encoding='utf-8') as outputs:
        for i in tp:
            outputs.write(i)

def remove_short(input_file,output_file):
    with open(input_file, 'r', encoding='utf-8') as inputs,open(output_file,'a',encoding='utf-8') as outputs:
        tp=[]
        for index, line in enumerate(inputs):
            t=line.split('|')
            if len(t[0])<2 or len(t[1])<2:
                outputs.write(line)
            else:tp.append(line)
    with open(input_file, 'w', encoding='utf-8') as outputs:
        for i in tp:
            outputs.write(i)

def remove_English(input_file,output_file):
    with open(input_file, 'r', encoding='utf-8') as inputs,open(output_file,'a',encoding='utf-8') as outputs:
        tp=[]
        for index, line in enumerate(inputs):
            t=line.split('|')
            if ''.join(t[0]).isalpha() or ''.join(t[1]).isalpha():
                outputs.write(line)
            else:tp.append(line)
    with open(input_file, 'w', encoding='utf-8') as outputs:
        for i in tp:
            outputs.write(i)

#remove_unknown(input_file,output_file,'娘泡')
replace_unknown(input_file,'','')
#remove_len(input_file,output_file)
#remove_short(input_file,output_file)
#remove_English(input_file,output_file)
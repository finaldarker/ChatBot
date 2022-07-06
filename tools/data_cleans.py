import sys
import re
import os

infile='../resources/chat_corpus/鲸梦.csv'
with open(infile, 'r', encoding='utf-8') as inputs:
    for index, line in enumerate(inputs):
        continue
count=index+1
#清洗成对符号
def remove_empty_paired_punc(in_str):
    return in_str.replace('()','').replace('《》','').replace('[]','').replace('【】','')

#清洗<br>等残留的HTML标签
def remove_html_tags(in_str):
    html_pattern=re.compile(r'<[^>]+>',re.S)
    return html_pattern.sub('',in_str)

def remove_common(symbol_first,symbol_second,in_str):
    if symbol_first and symbol_second in in_str:
        in_str=str(in_str)
        symbol_start=in_str.index(symbol_first)
        symbol_end=in_str.index(symbol_second)
        if in_str[-1]==str(symbol_second):
            in_str=in_str+'0'
        symbol=in_str[symbol_start:symbol_end+1]
        print(symbol)
        in_str=str(in_str).replace(symbol,'')
        return in_str
    else:return in_str
#清洗不可控制字符
'''
def remove_control_chars(in_str):
    control_chars=''.join(map(chr,list(range(0,32)))+list(range(127,160)))
    control_chars=re.compile('[%s]'%re.escape(control_chars))
    return control_chars.sub('',in_str)
'''
#输入文件
def evalute(input_file,output_file):
    with open(input_file, 'r', encoding='utf-8') as inputs,open(output_file, 'w', encoding='utf-8') as outputs:
        for index,line in enumerate(inputs):
            line=remove_common('{','}',line)
            outputs.write(line)
            if index%500==0:
                print(str(round(index/count*100,3))+'%')
    with open(output_file, 'r', encoding='utf-8') as pinputs,open(input_file, 'w', encoding='utf-8') as poutputs:
        for index, line in enumerate(pinputs):
            poutputs.write(line)

evalute(infile,'../resources/chat_corpus/鲸梦.txt')

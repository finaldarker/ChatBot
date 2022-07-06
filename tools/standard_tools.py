import os
import re
import jieba

file_path = os.path.abspath('../resources/chat_corpus/')
temp_path=os.path.abspath('../resources/Temp/')
corpus_name = "xiaohuangji"
corpus = os.path.join(file_path, corpus_name)

def printLines(file, n=10):
  with open(file, 'r', encoding='utf-8') as file_pipeline:
    for index, line in enumerate(file_pipeline):
      if index%2==0:
        qa=line.strip('M ').split()
      elif index%2==1:
        qb=line.strip('M ').split()
      else:continue

printLines(os.path.join(file_path, "xiaohuangji_temp.txt"))
word_wise = False  # True: 分词， False：分字
word_segmentation_path = os.path.join(temp_path, '{}_seg.txt'.format(corpus_name))  # 保存分词后的结果




def clean_zh_text(text):
  # 只保留数字，中文及常用中文标点（逗号/句号/感叹号/问号）
  comp = re.compile('[^0-9^\u4e00-\u9fa5^，。！？]')
  return comp.sub('', text)


def word_filter(words):
  # 去掉空字符，把jieba返回的生成器转化为字符串
  result = []
  for word in words:
    #word = clean_zh_text(word)
    if word == '':
      continue
    else:
      result.append(word)
  return ' '.join(result)


def cut_sentences(input_file, output_file):
  with open(input_file, 'r',encoding='utf-8') as input_pipeline, open(output_file, 'w',encoding='utf-8') as output_pipeline:
    for index, line in enumerate(input_pipeline):
      if index % 2 == 0:
        qa = line.strip().split()
        question = word_filter(jieba.cut(qa)if word_wise else qa)
      else :
        qb = line.strip().split()
        answer = word_filter(jieba.cut(qb) if word_wise else qb)
        result = '|'.join([question, answer])
        print(result)
        output_pipeline.write(result + '\n')


cut_sentences(os.path.join(file_path, "xiaohuangji_temp.txt"), word_segmentation_path)
printLines(word_segmentation_path)

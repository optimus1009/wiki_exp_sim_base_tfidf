# -*- coding: utf-8 -*-
# @Author  : lin.xiong

import jieba
import re
from zhon.hanzi import punctuation

mode_digit_alpha = re.compile(r"[0-9a-zA-Z\_]+")
emoji_pattern = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
    u"(\ud83c[\udf00-\uffff])|"  
    u"(\ud83d[\u0000-\uddff])|"  
    u"(\ud83d[\ude80-\udeff])|"  
    u"(\ud83c[\udde0-\uddff])"  
    "+", flags=re.UNICODE)
stopwords_list = []
with open('C:/Users/lin/Desktop/stopwords.data', 'r') as stopwordsfile:
    for stopword in stopwordsfile:
        stopwords_list.append(stopword.strip().decode('utf-8'))
stop_set = set(stopwords_list)
def segment(sentence, cut_all=True):
    '''
    :param sentence: 原始文本，字符串
    :param cut_all: 全模式
    :return: 用空格连接
    '''
    if type(sentence) == str:
        sentence = sentence.decode('utf-8')
        sentence = mode_digit_alpha.sub(r'', sentence) # 过滤数字，英文字母
        print 'sentence_1: ',sentence
        sentence = re.sub(ur"[%s]+" % punctuation, "", sentence) #过滤中文标点
        print 'sentence_2: ',sentence
        #sentence = re.sub(ur"[%s]+" %punctuation, "",sentence)
        return ' '.join(cut_word for cut_word in jieba.cut(sentence,HMM=True) if cut_word not in stop_set and len(cut_word) > 1) # 分词
    elif type(sentence) == unicode:
        sentence = mode_digit_alpha.sub(r'', sentence)  # 过滤
        sentence = re.sub(ur"[%s]+" % punctuation, "", sentence)
        return ' '.join(cut_word for cut_word in jieba.cut(sentence, HMM=True) if cut_word not in stop_set and len(cut_word) > 1)  # 分词
if __name__ == "__main__":
    cut_w = segment('穿上dfsfs米菲纸尿裤就爱笑32434的宝宝强提供。能遇到米菲真是幸运！！！')
    print cut_w
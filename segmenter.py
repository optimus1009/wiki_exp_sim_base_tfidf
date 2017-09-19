# -*- coding: utf-8 -*-
# @Author  : lin.xiong

import jieba
import re
from zhon.hanzi import punctuation

mode_digit_alpha = re.compile(r"[0-9a-zA-Z\_]+")
digit_alpha_pattern = re.compile(r"[A-Za-z0-9\[\`\~\!\@\#\$\^\&\?\...\】\【\!\《\》\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\!\@\#\\\&\*\%]")
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
        sentence = mode_digit_alpha.sub(r'', sentence) # 过滤
        sentence = digit_alpha_pattern.sub(r'',sentence)
        #sentence = re.sub(ur"[%s]+" %punctuation, "",sentence)
        return ' '.join(cut_word for cut_word in jieba.cut(sentence,HMM=True) if cut_word not in stop_set and len(cut_word) > 1) # 分词
    elif type(sentence) == unicode:
        sentence = mode_digit_alpha.sub(r'', sentence)  # 过滤
        sentence = digit_alpha_pattern.sub(r'', sentence)
        return ' '.join(cut_word for cut_word in jieba.cut(sentence, HMM=True) if cut_word not in stop_set and len(cut_word) > 1)  # 分词
if __name__ == "__main__":
    cut_w = segment('现在生活条件好，食物对于宝宝来说是43535gjfajgf随手可得的，加上家人朋友的疼爱，基本是想吃什么都能吃到。宝宝接触的食物越多，牙齿的护理又没有跟上，那么龋齿就慢慢的靠近了。宝宝龋齿，不仅会影响口腔健康和美观，还会对宝宝的胃肠功能产生一定的影响。所以爸妈们要格外重视宝宝的牙齿护理，从第一颗乳牙就开始清洁口腔和牙齿，保护好乳牙。除了龋齿这种常见的牙齿疾病，还有一种常见但是被忽略的牙齿疾病为脱矿。龋齿我们都知道，龋齿是因为牙釉质被酸性物质腐蚀，牙齿表面出现了坑洞，就是我们常说的蛀牙。但脱矿又是什么呢')
    print cut_w
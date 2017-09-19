# -*- coding: utf-8 -*-
# @Author  : lin.xiong

from __future__ import division
from segmenter import segment


class IDFLoader(object): 
    def __init__(self, idf_path):
        self.idf_path = idf_path
        self.idf_freq = {}     # idf
        self.mean_idf = 0.0    # 均值
        self.load_idf()

    def load_idf(self):       # 从文件中载入idf
        cnt = 0
        with open(self.idf_path, 'r') as f:
            for line in f:
                try:
                    word, freq = line.strip().split('\t')
                    cnt += 1
                except Exception as e:
                    pass
                self.idf_freq[word] = float(freq)

        print('Vocabularies loaded: %d' % cnt)
        self.mean_idf = sum(self.idf_freq.values()) / cnt #计算出所有idf的均值


class TFIDF(object): 
    def __init__(self, idf_path):
        self.idf_loader = IDFLoader(idf_path)
        self.idf_freq = self.idf_loader.idf_freq
        self.mean_idf = self.idf_loader.mean_idf

    def extract_keywords(self, sentence, topK=15):    # 提取关键词
        # 过滤
        seg_list = segment(sentence)
        freq = {}
        for w in seg_list.split():
            freq[w] = freq.get(w, 0.0) + 1.0
        if '' in freq:
            del freq['']
        total = sum(freq.values())

        for k in freq:   # 计算 TF-IDF,这里不产生异常，因为idf不存在则用平均值替代
            freq[k] *= self.idf_freq.get(k, self.mean_idf) / total


        tags = sorted(freq, key=freq.__getitem__, reverse=True)  # 排序

        if topK:
            return tags[:topK]
        else:
            return tags

idffile = 'C:/Users/lin/Desktop/idf.data'
tfidf = TFIDF(idffile)


def get_keyword(content):
    '''
    :param content: 原始文本
    :return: 关键字字符串，用空格连接，每个关键字类型是unicode字符
    '''

    sentence = content
    tags = tfidf.extract_keywords(sentence)
    return ' '.join(tags) #unicode


if __name__ == "__main__":
    with open('C:/Users/lin/Desktop/parse_wiki.data','r') as wiki_data:
        for line in wiki_data.readlines()[0:10]:
            line = line.strip().split('\t')[1]
            tag_string = get_keyword(line)
            print tag_string
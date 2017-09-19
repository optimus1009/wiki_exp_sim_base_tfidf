# -*- coding: utf-8 -*-
# @Author  : lin.xiong

import gensim
from gensim.models import Word2Vec

import segmenter
class sentences_generator():
    def __init__(self, file_path):
        self.filepath = file_path
    def __iter__(self):
        with open(self.filepath,'r') as input_file:
            for line in input_file:
                raw_sentence = line.strip().split('\t')[1]
                sentence = segmenter.segment(raw_sentence)
                yield [word for word in sentence.split()]  #['word_1','word_2','word_3']

total_sentence = []
for sent in sentences_generator('C:/Users/lin/Desktop/parse_wiki.data'):
    total_sentence.append(sent)
#训练模型
model = Word2Vec(total_sentence, size=100, window=5, min_count=5,workers=3)
#获取与单个词top-k相似度高的词语
#top_simi = model.most_similar([u'孩子'],topn=10)
#比较两个词的相似度
#model.wv.similarity('woman', 'man')
#存储模型
model.save('C:/Users/lin/Desktop/wiki_word2vec.model')
#加载模型
ew_model = gensim.models.Word2Vec.load('C:/Users/lin/Desktop/wiki_word2vec.model')

top_simi = ew_model.most_similar([u'孩子'],topn=15)




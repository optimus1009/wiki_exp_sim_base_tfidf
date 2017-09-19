# -*- coding: utf-8 -*-
# @Author  : lin.xiong

from __future__ import division
import gensim
import tfidf
import segmenter
from flask import Flask, request


#加载word2vec模型
model = gensim.models.Word2Vec.load('C:/Users/lin/Desktop/wiki_word2vec.model')

app = Flask(__name__)
@app.route('/api/get_similarity_score', methods=['GET', 'POST'])

def get_similarity_score():

    params = request.get_json(force=True)

    wiki_content = params['wiki']
    exp_content = params['exp']
    wiki_keyword = tfidf.get_keyword(wiki_content)
    wiki_keyword_simi = []
    for keyword in wiki_keyword.split():
        try:
            key_simi = model.most_similar([keyword],topn = 15)
            for elem in key_simi:
                wiki_keyword_simi.append(elem[0])
        except KeyError:
            continue
    wiki_cut = [word for word in segmenter.segment(wiki_content).split()]
    wiki_cut = wiki_cut + wiki_keyword_simi
    wiki_keyword_set  = set(wiki_cut)

    exp_cut = [word for word in  segmenter.segment(exp_content).split()]
    exp_set = set(exp_cut)
    intersection = len(wiki_keyword_set & exp_set)
    if len(exp_set) == 0:
        return str(0)
    else:
        return str(intersection/len(exp_set))

def main():
    app.run(host='192.168.35.169', port=12345)

if __name__ == '__main__':
    main()

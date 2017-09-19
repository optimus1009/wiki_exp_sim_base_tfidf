# -*- coding: utf-8 -*-
# @Author  : lin.xiong

from __future__ import division
import gensim
import tfidf
import segmenter

#加载word2vec模型
model = gensim.models.Word2Vec.load('C:/Users/lin/Desktop/wiki_word2vec.model')

def get_similarity_score(wiki,exp):
    wiki_content = wiki
    exp_content = exp
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
        return 0
    else:
        return intersection/len(exp_set)
if __name__ == '__main__':
    # out_put_file = open('C:/Users/lin/Desktop/out_wiki.data','w')
    # with open('C:/Users/lin/Desktop/wiki_test.data','r') as wikifile:
    #     for line in wikifile:
    #         wiki = line.strip().split('\t')[1]
    #         exp = line.strip().split('\t')[2]
    #         for exp_elem in exp.split('|'):
    #             simi_score = get_similarity_score(wiki,exp_elem)
    #             out_put_file.write(wiki + ' \t' + exp_elem + '\t' + str(simi_score) + '\n')
    # out_put_file.close()
    wiki = '宝宝刚学习走路时，多用脚掌前端的力量，脚步岔开，甚至会比肩膀还宽，摇摇晃晃的，这就是所谓的姗姗学步。有些宝宝为了支撑身体重量的平衡，会出现外八字步态，这种姿势在3-4岁左右就会慢慢恢复。如果宝宝3-4岁之后，走路还像唐老鸭般出现外八字步态，就要注意是否髋关节的问题了。尽早去专科医院检查。	小孩小的时候走八路，我觉得要么大人背多了，要么还没到走路的年龄早早开始锻炼也有关吧，大人都有一定关系的|长大一点就好了吧！我感觉说这事习惯问题吧！有时候大人也会出现这种情况吧！多纠正，穿合适的鞋子。|小孩外八字，绝对会影响以后走路的。走路姿势不正确，还是应该及早让他修正过来。不能长大了就后悔|走八路应该是小时候腿经常弯曲吧以前从来不去评论浪费了很多积分。现在才知道积分可以抵用现金。就要好好评论，后来把这段文字复制下来，买到哪评到哪。用用来充文字数。即能赚积分还省事，最重要的是再也不用费劲评价不用去想还差多少字了。直接复制粘贴发出去就行了。超级方便使用，但乳类仍是宝宝每天应该选择的，科学合理的幼儿配方奶粉可延续母乳的好处，继续为宝宝提供丰富的营养，13个月宝宝每天可以喝300'
    exp = '宝宝刚学习走路时，多用脚掌前端的力量，脚步岔开，甚至会比肩膀还宽，摇摇晃晃的，这就是所谓的姗姗学步'
    score = get_similarity_score(wiki,exp)
    print score


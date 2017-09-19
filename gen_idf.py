# -*- coding: utf-8 -*-
# @Author  : lin.xiong

from  __future__ import division
import math
import datetime

from segmenter import segment

class MyDocuments(object):    # 基于python生成器的实现yield可以高效读取文件,https://www.ibm.com/developerworks/cn/opensource/os-cn-python-yield/
    def __init__(self, inputfile):
        self.inputfile = inputfile
 
    def __iter__(self):
        text = open(self.inputfile, 'r').readlines()
        for line in text:
            line = line.strip().split('\t')[1]
            yield segment(line)   # time consuming


def get_idf(inputfile,idffile):   # idf generator

    inputfile = inputfile
    outputfile = idffile

    doc = []
    with open(inputfile,'r') as ins:
        for line in ins:
            line = line.strip().split('\t')[1]
            doc.append(segment(line))

    id_freq = {}
    i = 0
    for cut_doc in doc:
        #print "doc: ",doc
        for x in cut_doc.split():
            id_freq[x] = id_freq.get(x, 0) + 1
        if i % 1000 == 0:
            print('Documents processed: ', i, ', time: ', 
                datetime.datetime.now())
        i += 1

    with open(outputfile, 'w') as f:
        for key, value in id_freq.items():
            f.write(key.encode('utf-8') + '\t' + str(math.log(i / value + 1, 2)) + '\n')

    
if __name__ == "__main__":
    wiki_file = 'C:/Users/lin/Desktop/parse_wiki.data'
    idffile = 'C:/Users/lin/Desktop/idf.data'
    get_idf(wiki_file,idffile)

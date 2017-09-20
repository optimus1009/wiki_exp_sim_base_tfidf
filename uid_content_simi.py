# -*- coding: utf-8 -*-
# @Author  : lin.xiong

from __future__ import division
import segmenter

out_file =  open('C:/Users/lin/Desktop/out_uid_content.data','w')
with open('C:/Users/lin/Desktop/uid_content.data','r') as uid_content_file:
    for line in uid_content_file:
        line = line.strip()
        uid = line.split('\t')[0]
        comment_list = line.split('\t')[1].split('|')
        comment_arr = []
        union_comment = set()
        if len(comment_list) < 2:
            out_file.write(uid + '\t' + '-1' + '\t' + '1' +'\n')
        else:
            for comment in comment_list:
                comment_set = set(segmenter.segment(comment).split())
                comment_arr.append(comment_set)
                union_comment |= comment_set

            inter_comment = reduce(lambda x ,y : x & y, comment_arr)
            if len(union_comment) == 0:
                simi = 1
            else:
                simi = len(inter_comment)/len(union_comment)
            out_file.write(uid + '\t' + str(simi) + '\t' + str(len(comment_list)) + '\n')
out_file.close()
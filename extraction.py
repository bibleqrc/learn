# -*- coding: utf-8 -*-
#from project.docs_retrieve.docs_process import *
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
middlePath = os.path.split(curPath)[0]
rootPath = os.path.split(middlePath)[0]
sys.path.append(rootPath)
sys.path.append(middlePath)
import operator
from project.nlp_handle.docs_split import sentence_splitter
from project.nlp_handle.sentence_process import sentence_process
from similarity.get_similarity_between_sentences import sentences_similarity
from project.docs_retrieve.docs_process import search

def answer_extract(query,fragment):
    fragment = fragment.replace(" ","")
    fragment = fragment.replace("\n","")
    sentences = sentence_splitter(fragment)
    sentences_rank = {}
    top_ten = []
    core,core_depen = sentence_process(query)
    for sentence_index in xrange(0,len(sentences)):
        # print "sentence_index:",sentence_index
        # print "sentence:",sentences[sentence_index]
        sentences_rank[sentence_index] = 0.0
        try:
          core2,core2_depen = sentence_process(sentences[sentence_index])
        except:
          continue
        sentences_rank[sentence_index]= sentences_similarity(core1=core,core1_dependency=core_depen,core2=core2,core2_dependency=core2_depen)

    #根据相似度对候选句子进行排序
    sorted_sentence_rank = sorted(sentences_rank.items(), key=operator.itemgetter(1), reverse=True)

    # 选择相似度最靠前的五个句子返回
    item_count = 0
    for (sentence_index, score) in sorted_sentence_rank:
        top_ten.append(sentences[sentence_index])
        item_count += 1

        if item_count >= 10:
            break
    return top_ten

if __name__ == "__main__":
    print "答案抽取检测，请输入问题"
    while 1:
      query = raw_input(">")
      fragment = search(query)
      #print fragment
      answers = answer_extract(query,fragment)
      for each in answers:print each

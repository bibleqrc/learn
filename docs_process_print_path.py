# -*- coding: utf-8 -*-
import operator
import os
import sys
import time
from math import log

import config
from db.DBHelper import *
from helper import helper

curPath = os.path.abspath(os.path.dirname(__file__))
middlePath = os.path.split(curPath)[0]
rootPath = os.path.split(middlePath)[0]
sys.path.append(rootPath)
from project.question_analysis.keywords_extract import keywords_extract

def search(query):
    # 第一种处理查询的方式
    #query_list = jieba.cut(query)
    # 第二种查询方式的方式
    query_list = keywords_extract(query)
    fragments = top_ten_docs(query_list)
    return fragments

def get_docs_path(query):
    query_list = keywords_extract(query)
    paths = top_ten_docs(query_list)
    return paths

def top_ten_docs(query):
    """
    search docs from database
    :param query the query is a list
    :return:
    """
    # query = [x.encode("utf8") for x in query]
    top_ten = []
    start = time.time()
    s_vec = {}
    for k in query:
        if s_vec.has_key(k):
            s_vec[k] += 1
        else:
            s_vec[k] = 1


    helper.log("using %ss to vector %s "%(time.time() - start, ",".join(query)))

    start = time.time()
    average_len = get_docs_average_len()
    doc_count = get_docs_count()
    helper.log("using %ss to get average length and docs count"%(time.time() - start))

    doc_rank = {}
    doc_term_count = {}
    doc_length = {}
    term_dic = {}


    start = time.time()

    doc_list_result = []
    pre_doc_list_result = []
    doc_list_result_init = False
    for word in s_vec.keys():

        # for each word add {term_id}->{ "term"=> {term}, "doc_frequency"=> {doc_frequency} } into term_dic
        # get docs which contain these word
        # add doc_id -> 0 into docs_rank dictionary
        # add {doc_id}-{term_id} -> count into doc_term_count dictionary
        # if doc_id not exists in doc_length, get doc_length and save {doc_id}->{doc_length} into doc_length

        t = term()
        d_t = doc_term()
        # 获取关键词word在数据库表中的id
        term_id = t.get_term_id(word)
        print term_id
        if term_id == 0:
            continue
        t.ini_by_term_id(term_id)
        term_dic[term_id] = {"term": t.term, "doc_frequency": t.doc_frequency}

        doc_term_list = d_t.get_doc_term_list_by_term_id(term_id)

        doc_id_list = [d.doc_id for d in doc_term_list]
        # 获取文档的id列表
        if doc_list_result_init:
            # 去除列表中重复的ID
            pre_doc_list_result = doc_list_result
            doc_list_result = list(set(doc_list_result) & set(doc_id_list))

        else:
            doc_list_result = doc_id_list
            doc_list_result_init = True

        #如果这个循环处理后的list为0,则去上一个循环处理的list
        #如果这个循环处理后的list小于10,则去上一个循环处理的list
        if len(doc_list_result)<11:
            doc_list_result = pre_doc_list_result

        for doc_term_item in doc_term_list:
            if doc_term_item.doc_id in doc_list_result and doc.check_term_exist_by_id(doc_term_item.doc_id):
                doc_term_count["%d-%d"%(doc_term_item.doc_id, doc_term_item.term_id)] = doc_term_item.count

    print "second"

    #当doc_result_list为0的时候，取其为query中第一个词语也即是关键词抽取出来的最重要的词的文档作为doc_list_result
    if len(doc_list_result)==0:
        word = query[0]
        t = term()
        d_t = doc_term()
        # 获取关键词word在数据库表中的id
        term_id = t.get_term_id(word)
        print term_id
        if term_id != 0:
            t.ini_by_term_id(term_id)
            term_dic[term_id] = {"term": t.term, "doc_frequency": t.doc_frequency}
            doc_term_list = d_t.get_doc_term_list_by_term_id(term_id)
            doc_id_list = [d.doc_id for d in doc_term_list]
            doc_list_result = doc_id_list

    for i in doc_list_result:
        doc_rank[i] = 0

    print len(doc_rank.keys())
    for doc_item_id in doc_rank.keys():
        d = doc()
        d.ini_by_id(doc_item_id)
        doc_length[doc_item_id] = d.doc_len

    helper.log("using %s s to gather all the data"%(time.time() - start))

    #calculate the rank result1

    end = time.time()
    M = doc_count
    k = config.BM25.TF_Transformation_k
    b = config.BM25.Length_Normalization_b
    average_len = int(get_docs_average_len())

    print "begin calculate in local,","cost time :",end-start

    for doc_id in doc_rank.keys():
        score = 0
        for term_id in term_dic.keys():
            doc_term_id = "%d-%d"%(doc_id, term_id)
            if doc_term_id in doc_term_count.keys():

                c_w_q = s_vec[term_dic[term_id]["term"]]     #查询中这个词语的数目
                c_w_d = doc_term_count[doc_term_id]

                d_len = doc_length[doc_id]

                d_f_w = term_dic[term_id]["doc_frequency"]

                doc_term_score = c_w_q * c_w_d * (k + 1) * 1.0
                doc_term_score /= (c_w_q + k*(1 - b + b * d_len / average_len))
                doc_term_score *= log((M + 1) * 1.0 / d_f_w)
                score += doc_term_score
        doc_rank[doc_id] = score
    sorted_doc_rank = sorted(doc_rank.items(), key = operator.itemgetter(1),reverse=True)
    helper.log("using %ss to calculate the score of all relevative docs"%(time.time() - start))

    item_count = 0
    for (doc_id, score) in sorted_doc_rank:
        d = doc()
        d.ini_by_id(doc_id)
        top_ten.append(d.doc_path)
        item_count += 1

        if item_count >= 10:
            break
    for each in query:
        path = '/home/qrc/code/qaDemo/WikiQA/WikiQA_DATA/data/fragment//' + each + '\n.md'
        if os.path.exists(path) and path not in top_ten:
            top_ten.append(path)
    # for each in top_ten:print  each.replace('\n','')
    return [each.replace('\n','') for each in top_ten]


if __name__ =='__main__':
    print '文档检索检测，请输入问题：'
    while 1:
        question = raw_input(">")
        paths = get_docs_path(question)
        print "检索到的文档路径："
        for path in paths:
            print  path



# if __name__ == '__main__':
#     data_set_path = middlePath + '/data_set_handle/retrieve/random_question'
#     print data_set_path
#
#     # f = open('/home/qrc/code/qaDemo/WikiQA/WikiQA_DATA/data/fragment//法定结婚年龄\n.md')
#
#     with open(data_set_path + '/question_set_5') as f_read:
#         with open(data_set_path + '/question_set_path_5', 'w') as f_write:
#             lines = f_read.readlines()
#             for each in lines:
#                 each = each.replace('\n', '').strip()
#                 # print each,len(each)
#                 if len(each) != 0:
#                     #print each
#                     query_list = keywords_extract(each)
#                     ten = top_ten_docs(query_list)
#                     f_write.write(each+'\n')
#                     for d in ten:
#                         #print d.doc_path
#                         f_write.write(d.encode('utf8').replace('\n', '') + '\n')
#                     f_write.write('\n\n')
#
#                     # print each
#                     #detect = detect_query(each)
#                     # print each,'  ',detect
#                     #f_write.write(each + ' ' + detect + '\n')

# if __name__ == "__main__":
#     # queries = ['《本草纲目》写于哪一年','姚明的父亲姚志源多高',
#     #            '欧洲的第一所大学是','世界最大的流动性沙漠是','国际海洋法的总部位于哪个国家',
#     #            '经典力学的基础是','中央电视台拥有多少个电视频道']
#     #queries = ['马尔代夫的第一大支柱产业是什么','马达加斯加位于哪个大洲']
#     #queries = ['路由器位于OSI模型哪一层','华南理工大学在哪里','我国第一部文学理论和评论专着是南北朝时期刘勰的哪本着作？']
#     #queries = ['火药是哪国人发明的','端午节是哪天','WTO是哪个组织的称呼','赞比亚使用哪种货币']
#     # queries = ['市场经济的含义是什么','国际比赛规定，马拉松的全程距离约为多少公里','交通事故报警电话是多少'
#     #            ,'人类合成的第一种抗菌药是']
#     # queries =  ['肚皮舞起源于哪个国家','图灵是哪个国家的','抗日战争时期百团大战的指挥官主要是哪位八路军副总司令'
#     #            ,'招商融资有哪些途径','毛泽东弟弟是谁']
#     # queries = ['武汉腐乳是用什么发酵的','哪部电影是唯一一部获得奥斯卡最佳外语片的华语电影',
#     #            '截拳道是谁创立的一类现代武术体系','中国历史上规模最大的一套丛书是？']
#     # queries = ['图书馆学最早由谁提出','紫外线的波长大约在什么范围内','俄狄浦斯的父母是','格林兰岛属哪国',
#     #            '小米公司ceo是谁','古巴的首都在哪个城市','空想社会主义学说的代表人物有哪些']
#     queries = ['1907年起，开始以粉色的什么花作为母亲节的象征？','地球上最曲折的山在哪里','“宽窄巷子”是我国西南哪个城市的三大历史保护区之一？',
#                '世界最重要的IT高科技产业基地，惠普公司总部所在地“硅谷”位于哪个国家？','哈尔滨以什么著称','自行车大约于哪一年传入中国？',
#                '《资治通鉴》的撰写一共耗时多少年？']
#
#     # 总的合并问题
#     # queries = ['市场经济的含义是什么','国际比赛规定，马拉松的全程距离约为多少公里','交通事故报警电话是多少','人类合成的第一种抗菌药是',
#     #            '肚皮舞起源于哪个国家', '图灵是哪个国家的', '抗日战争时期百团大战的指挥官主要是哪位八路军副总司令'
#     #            ,'招商融资有哪些途径','毛泽东弟弟是谁''武汉腐乳是用什么发酵的', '哪部电影是唯一一部获得奥斯卡最佳外语片的华语电影',
#     #           '截拳道是谁创立的一类现代武术体系','中国历史上规模最大的一套丛书是？','图书馆学最早由谁提出','紫外线的波长大约在什么范围内','俄狄浦斯的父母是','格林兰岛属哪国',
#     #         '小米公司ceo是谁','古巴的首都在哪个城市','空想社会主义学说的代表人物有哪些',
#     #            '1907年起，开始以粉色的什么花作为母亲节的象征？', '地球上最曲折的山在哪里', '“宽窄巷子”是我国西南哪个城市的三大历史保护区之一？',
#     #           '世界最重要的IT高科技产业基地，惠普公司总部所在地“硅谷”位于哪个国家？','哈尔滨以什么著称','自行车大约于哪一年传入中国？',
#     #           '《资治通鉴》的撰写一共耗时多少年？'
#     #            ]
#     file = open("result2_7", "a")
#     for query in queries:
#         #query = "《本草纲目》撰成于哪一年"
#         try:
#          docs = search(query)
#         except:
#          continue
#         # print "begin docs"
#         # print docs
#         # print "end docs"
#         # print len(sentence_splitter(docs))
#         print query
#         start = time.time()
#         answers = answer_extract(query,docs)
#         cost = time.time()-start
#         print "cost time:",cost
#
#         file.write(query)
#         file.write('\n')
#         file.write(str(cost))
#         file.write('\n')
#         for a in answers:
#             print a
#             file.write(a)
#             file.write('\n')
#         file.write('\n\n')
#     file.close()


if __name__ =='__main__':
    question = '姚明的父亲姚志源多高'
    paths = get_docs_path(question)
    for path in paths:
        print  path
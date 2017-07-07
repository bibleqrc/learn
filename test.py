# # -*- coding: utf-8 -*-
# from pyltp import SentenceSplitter
# from pyltp import Segmentor
# from pyltp import Postagger
# from pyltp import SementicRoleLabeller
# from pyltp import NamedEntityRecognizer
# from pyltp import Parser
# #from projectTest import ltp_model_loader
# from nlp_handle import ltp_model_loader
# from nlp_handle.extract_focus import *
# import fileinput
# import jieba
#
# stopwords = [line.strip().decode('utf-8')
#              for line in fileinput.input(ltp_model_loader.STOPWORDS_FILE)]
#
#
# #测试分词
# #words = segmentor('我家在昆明，我现在在北京上学。中秋节你是否会想到李白？还有，微博是MebiuW')
# words = segmentor('许多优秀的人才都被送往国外学习。')
# print('###############以上为分词测试###############')
# #测试标注
# tags = posttagger(words)
# print('###############以上为词性标注测试###############')
# #依存句法识别
# arcs = parse(words,tags)
# print('###############以上为依存句法测试###############')
#
# #获取核心词和核心词的依存词
# count = extract_first_and_second(words,arcs)
# #获取核心词
# print  count.keys()[0],[i for i in count.values()[0]]
# #获取依存词
# for i in count.values()[0]:
#     print i
#
#
# words = segmentor('中秋节你是否会想到李白？')
# tags = posttagger(words)
# arcs = parse(words,tags)
# count2 = extract_first_and_second(words,arcs)
#
#
# #获取核心词
# print  count.keys()[0],[i for i in count.values()[0]]
# #获取依存词
# for i in count.values()[0]:
#     print i
#
# #获取核心词
# print  count2.keys()[0],[i for i in count2.values()[0]]
# #获取依存词
# for i in count2.values()[0]:
#     print i



similarity_matrix = [ [1,2,3],[1,2,1]]
max_similarty_m_sum = 0
max_similarty_m = 0
for m in range(0,2):
    max_similarty_m = similarity_matrix[m][0]
    for n in range(0, 3):
        if  max_similarty_m < similarity_matrix[m][n]:
            max_similarty_m = similarity_matrix[m][n]

    max_similarty_m_sum = max_similarty_m_sum + max_similarty_m
    print "max:", max_similarty_m
    print "max_sum:", max_similarty_m_sum
similarity_s1_to_s2 = max_similarty_m_sum/m
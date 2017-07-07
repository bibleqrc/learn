# -*- coding: utf-8 -*-
from get_similarity_between_words import get_sim
#a,b代表权重，可以自定义
# a = 0.5
# b = 0.5
# a = 0.6
# b = 0.4
# a = 0.65
# b = 0.35
# a = 0.7
# b = 0.3
# a = 0.45
# b = 0.55
a = 0.4
b = 0.6
def get_similarity_matrix(core1_denpendency,core2_denpendency):
    length_m = len(core1_denpendency)
    length_n = len(core2_denpendency)
    # for each in core1_denpendency:print each
    # for each in core2_denpendency:print each
    similarity_matrix = []
    for m in range(0, length_m):
        similarity_matrix.append([])
        for n in range(0, length_n):
            # print core1_denpendency[m],core2_denpendency[n]
            # print get_sim(core1_denpendency[m], core2_denpendency[n])
            similarity_matrix[m].append(get_sim(core1_denpendency[m],core2_denpendency[n]))
    return similarity_matrix

def sentences_similarity(core1,core1_dependency,core2,core2_dependency):
    #计算核心词的相似度
    similarity1 = get_sim(core1,core2)
    #print "similaroty1:",similarity1
    similarity_matrix = get_similarity_matrix(core1_dependency,core2_dependency)
    similarity2 = 0
    length_m = len(core1_dependency)
    length_n = len(core2_dependency)
    if length_m ==0 or length_n ==0:
        similarity2 = 0.0
    else:
        max_similarty_m_sum = 0
        #max_similarty_m = 0
        for m in xrange(0,length_m):
            max_similarty_m = similarity_matrix[m][0]
            for n in xrange(0, length_n):
                if  max_similarty_m < similarity_matrix[m][n]:
                    max_similarty_m = similarity_matrix[m][n]
            max_similarty_m_sum = max_similarty_m_sum + max_similarty_m
        similarity_s1_to_s2 = max_similarty_m_sum/length_m
        #print "max_similarty_m_sum:", max_similarty_m_sum, "  ", "m: ", length_m
        #print "similarity_s1_to_s2:",similarity_s1_to_s2

        max_similarty_n_sum = 0
        for n in xrange(0,length_n):
            max_similarty_n = similarity_matrix[0][n]
            for m in xrange(0, length_m):
                if max_similarty_n < similarity_matrix[m][n]:
                   max_similarty_n = similarity_matrix[m][n]
            max_similarty_n_sum =max_similarty_n_sum + max_similarty_n
        similarity_s2_to_s1 = max_similarty_n_sum/length_n
        #print "max_similarty_n_sum:", max_similarty_n_sum, "  ", "n: ", length_n
        #print "similarity_s2_to_s1:",similarity_s2_to_s1

        similarity2 = (similarity_s1_to_s2+similarity_s2_to_s1)/2
    #print "similarity2:",similarity2

    similarity = a*similarity1 + b*similarity2
    #print similarity1,float(similarity2)
    return float(similarity)

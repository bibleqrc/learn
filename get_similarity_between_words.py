# -*- coding: utf-8 -*-


from gensim.models import Word2Vec
import chardet
#model = Word2Vec.load("/home/qrc/chatbotMaterial/wiki.zh.text.model")
#model = Word2Vec.load("D:\qa_material\wiki.zh.text.model")
#model = Word2Vec.load("D:\qa_material\model\wiki.zh.text.model")

from os import path
MODEL_PATH = path.normpath(path.join(path.dirname(path.abspath(__file__)), '../../../model/wiki.zh.text.model'))
print MODEL_PATH
model = Word2Vec.load(MODEL_PATH)

#print model[u'男人']
#print model.most_similar(u"女人")[0][0]
# print  model.similarity(u"女人",u"男人")
#
# #print model.most_similar(u"足球")
#
# print  model.similarity("女人".decode("utf-8"),"男人".decode("utf-8"))
#
# print model.most_similar(u"足球")

# print chardet.detect("男人")
# print u"男人"
# print "男人".decode("utf-8")
#print "男人".decode()
#
# print chardet.detect("男人")
# print chardet.detect("男人")['encoding']
def get_sim(a,b):
    if a == None:
        return 0.0
    if b == None:
        return 0.0
    if chardet.detect(a)['encoding']=='utf-8':
         a=a.decode("utf-8")
    # elif chardet.detect(a)['encoding'] == 'windows-1252':
    #     a = a.decode("windows-1252")
    if chardet.detect(b)['encoding']=='utf-8':
         b=b.decode("utf-8")
    # elif chardet.detect(b)['encoding'] == 'windows-1252':
    #     b = b.decode("windows-1252")
    # if chardet.detect(a)['encoding'] == 'windows-1252':
    #     a = a.decode("windows-1252")
    # if chardet.detect(b)['encoding'] == 'windows-1252':
    #      b = b.decode("windows-1252")
    #return model.similarity(a,b)
    try:
      return model.similarity(a,b)
    except:
      return 0.0

def get_sim_max_pooling(a,l):
    ansl=[]
    if (not isinstance(a,str)) and isinstance(a,list):
        for c in a:
            for b in l:
                ansl.append(get_sim(b,c))
    else:
        for b in l:
            ansl.append(get_sim(a,b))
    if len(ansl)==0:
        return 0;
    return max(ansl)

def get_sim_mean_pooling(a,l):
    ansl=[]
    for b in l:
        ansl.append(get_sim(a,b))
    if len(ansl)==0:
        return 0
    return sum(ansl)/len(ansl)

if __name__ == "__main__":
    # print chardet.detect("人才")
    # print chardet.detect("北京")
    # print get_sim("男人","女人")
    # print model.most_similar("人才".decode("utf-8"))[0][0]
    # print model.most_similar("中国".decode('utf-8'))[0][0]
    #
    print model.most_similar(u"威海")[0][0]
    ## print model.most_similar(u"将")[0][0]
    # print model.most_similar(u"基础")[0][0]
    # print model.most_similar(u"加速")[0][0]
    # print model.most_similar(u"一个")[0][0]
    # print model.most_similar(u"还")[0][0]
    # print model.most_similar(u"将")[0][0]
    # print model.most_similar(u"于")[0][0]
    # print model.most_similar(u"于是")[0][0]
    # print model.most_similar(u"分别")[0][0]
    # print model.most_similar(u"同时")[0][0]
    # print model.most_similar(u"通过")[0][0]
    # print model.most_similar(u"石化")[0][0]
    #print model.most_similar(u"进军")[0][0]
    # print chardet.detect("都")
    # print get_sim("都","国外")
    print get_sim("大人","小孩")
    # print get_sim("足球","篮球")


# -*- coding: utf-8 -*-
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import SementicRoleLabeller
from pyltp import NamedEntityRecognizer
from pyltp import Parser
from project import ltp_model_loader
import fileinput
import jieba

stopwords = [line.strip().decode('utf-8')
             for line in fileinput.input(ltp_model_loader.STOPWORDS_FILE)]

def _remove_stopwords(words):
    """  去停用词，默认停用词表仅包含中英文常用标点符号
    :param words: 分词结果
    :return: 去停用词后的词列表
    """
    for word in words:
        if word in stopwords:
            words.remove(word)
    return words

#分词
def segmentor(sentence='你好，你觉得这个例子从哪里来的？当然还是直接复制官方文档，然后改了下这里得到的。我的微博是MebiuW，转载请注明来自MebiuW！'):
    segmentor = Segmentor()  # 初始化实例
    ltp_model_loader.load(segmentor)   # segmentor.load('C:\\Users\\72770\\Documents\\Chatbot\\ltp-data-v3.3.1\\ltp_data\\cws.model')  # 加载模型
    #使用pyltp分词
    # words = segmentor.segment(sentence)  # 分词
    # #print '\t'.join(words) #默认可以这样输出
    # words_list2 = list(words) # 可以转换成List 输出
    # words_list2 = _remove_stopwords(words_list2)
    #使用jieba分词   经过测试jieba分词的效果更好，所以使用jiaba分词
    words_list = _remove_stopwords(jieba.lcut(sentence))
    print type(words_list)
    for each in words_list:print each,type(each),each.encode('utf-8')
    segmentor.release()  # 释放模型
    return [each.encode('utf-8') for each in words_list]

def posttagger(words):
    postagger = Postagger() # 初始化实例
    ltp_model_loader.load(postagger)
    #postagger.load('C:\\Users\\72770\\Documents\\Chatbot\\ltp-data-v3.3.1\\ltp_data\\pos.model')  # 加载模型
    postags = postagger.postag(words)  # 词性标注
    #postags = postagger.postag([i.encode('utf-8') for i in words])
    # for word,tag in zip(words,postags):
    #     print word+'/'+tag
    postagger.release()  # 释放模型
    return postags


#依存语义分析
def parse(words, postags):
    parser = Parser() # 初始化实例
    ltp_model_loader.load(parser)
   #parser.load('C:\\Users\\72770\\Documents\\Chatbot\\ltp-data-v3.3.1\\ltp_data\\parser.model')  # 加载模型
    arcs = parser.parse(words, postags)  # 句法分析

    print "\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs)
    #print len(arcs)
    parser.release()  # 释放模型
    return arcs

def extract_first_and_second(words,arcs):
    counts = [{words[i]:[]}for i in range (0,len(words))]
    for  i in range(0,len(arcs)):
        #print words[i],words[arcs[i].head],counts[arcs[i].head].keys()[0]
        if arcs[i].head < len(arcs):
            #print words[i], words[arcs[i].head], counts[arcs[i].head].keys()[0]
            counts[arcs[i].head][words[arcs[i].head]].append(words[i])
    for i in range(0,len(words)):
        print counts[i].keys()[0]
        print "begin"
        for a in counts[i][words[i]]:print a
        print "over"
    retu = 0
    index = 0
    for i in range(0,len(counts)):
        num = len(counts[i].values()[0])
        #print len(counts[i].values()[0])
        if num>retu:
            retu=num
            index=i
    # print index
    # print counts[index]
    if words[index] in counts[index].values()[0]:
        counts[index][words[index]].remove(words[index])
    return counts[index]
    #print [count[i].keys() for i in range(0,len(words))]


#测试分词
#words = segmentor('我家在昆明，我现在在北京上学。中秋节你是否会想到李白？还有，微博是MebiuW')
words = segmentor('许多优秀的人才都被送往国外学习。')
print('###############以上为分词测试###############')
#测试标注
tags = posttagger(words)
print('###############以上为词性标注测试###############')
#依存句法识别
arcs = parse(words,tags)
print('###############以上为依存句法测试###############')

#获取核心词和核心词的依存词
count = extract_first_and_second(words,arcs)
#获取核心词
print  count.keys()[0],[i for i in count.values()[0]]
#获取依存词
for i in count.values()[0]:
    print i


words = segmentor('中秋节你是否会想到李白？')
tags = posttagger(words)
arcs = parse(words,tags)
count2 = extract_first_and_second(words,arcs)


#获取核心词
print  count.keys()[0],[i for i in count.values()[0]]
#获取依存词
for i in count.values()[0]:
    print i

#获取核心词
print  count2.keys()[0],[i for i in count2.values()[0]]
#获取依存词
for i in count2.values()[0]:
    print i
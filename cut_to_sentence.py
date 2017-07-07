# -*- coding: utf-8 -*-
from pyltp import SentenceSplitter
#分句，也就是将一片文本分割为独立的句子
def sentence_splitter(sentence='你好，你觉得这个例子从哪里来的？当然还是直接复制官方文档，然后改了下这里得到的。'):
    sents = SentenceSplitter.split(sentence)  # 分句
    #print '\n'.join(sents)
    return ['\n'.join(sents)]

#测试分句子
sentence_splitter()
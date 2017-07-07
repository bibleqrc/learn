# -*- coding: utf-8 -*-
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
middlePath = os.path.split(curPath)[0]
rootPath = os.path.split(middlePath)[0]
sys.path.append(rootPath)
from project.nlp_handle.docs_reading import read_doc
from project.nlp_handle.docs_split import *
from project.answer_extraction.extraction import *


def get_fragment(doc_paths):
    result_fragment = []

    for doc_path in doc_paths:
        try:
            fragment_doc = read_doc(doc_path)
            result_fragment.append(fragment_doc)
        except:
            print "can not open %s" % doc.doc_path
    return ''.join(result_fragment)

if __name__ == '__main__':
    data_set_path = middlePath + '/data_set_handle/retrieve/57_not/'+'qa_not_read_'+str(21)
    doc_result_path = middlePath + '/data_set_handle/retrieve/57/'+'qa_read_'+str(21)
    #data_set_path = middlePath + '/data_set_handle/retrieve/other_paths/' + 'other_path_' + str(5)
    #doc_result_path = middlePath + '/data_set_handle/retrieve/other_read/' + 'other_read_' + str(5)
    print data_set_path
    print doc_result_path

    with open(data_set_path) as file_read:
        lines = file_read.readlines()
        title = ''
        doc_paths = []
        for line in lines:
            line = line.replace('\n',"")
            print line,'  ', len(line)
            #print len(line)
            if len(line)!=0:   #或者为1
                #print line, '  ', len(line)
                if '.md' not in line:
                   title = line
                   # print 'title:',title
                else:
                    index = line.find('.md')
                    doc_path = line[:index]+'\n.md'
                    doc_paths.append(doc_path)
            else:
                # print "here"
                #
                doc_content = get_fragment(doc_paths)
                start = time.time()
                answers = answer_extract(title, doc_content)
                cost = time.time() - start
                print "cost time:", cost
                
                with open(doc_result_path, "a") as file_write:
                    file_write.write(title+'\n')
                    file_write.write(str(cost)+'\n')
                    for a in answers:
                        print a
                        file_write.write(a+'\n')
                    file_write.write('\n\n')


                # print 'title::::',title
                # print "doc_paths:"
                # for each in doc_paths:print each


                title=''
                doc_paths=[]



            # 拼接路径
            # index =  line.find('.md')
            # print index,line[:index]
            # print line[:index]+'\n.md'

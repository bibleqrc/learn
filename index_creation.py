# -*- coding: utf-8 -*-
import os
import config
from db.DBHelper import *
from helper import helper
import jieba

def docs_to_vector(docs):
    """
    case insensitive

    :param docs: the docs is a fragment string
    :return: dictionary

    """
    docs = docs.lower()

    set_list = jieba.cut(docs)
    result = {}
    for term in set_list:
        if term in config.stop_word:
            continue
        if term in result.keys():
            result[term] += 1
        else:
            result[term] = 1
    return result

def scan_files(files_dir):
    """
    :param files_dir: the directory which contains fragments
            file_name_list: the filename list
    :return:
    """

    last_counter_id = 0
    try:
        f = open(config.log_file)
        line = f.read()
        f.close()
        last_counter_id = int(line.split(" ")[0])
    except:
        pass
    file_counter = 0
    for file_name in os.listdir(files_dir):
        if file_name[0] == '.':
            continue
        file_counter += 1
        if file_counter % 100 == 0:
            print "%d processed file %s" % (file_counter, file_name)
        if file_counter < last_counter_id:
            print "skip %d" % file_counter
            continue
        file_path = files_dir + "/" + file_name
        process(file_path)
        helper.log("%d processed file %s"%(file_counter, file_path))

def process(file_path):
    """
    :param file_path: the file path which is needed to process
    :return:None
    """
    try:
        doc_file = open(file_path,"r")
        docs = doc_file.read()
        doc_file.close()
    except:
        return

    doc_len = len(docs)
    d = DBHelper()

    doc_id = d.insert_record_with_var("insert into wiki_doc(`doc_len`,`doc_path`) VALUES (%s,%s)",(doc_len,file_path))
    d = docs_to_vector(docs)
    t = term()
    d_t = doc_term()
    for word in d:
        if word not in stop_word:
            term_id = 0
            if t.check_term_exist(word):
                term_id = t.get_term_id(word)
            else:
                term_id = t.insert_term(word,0)
            t.add_term_frequency(word)
            d_t.insert_record(term_id,doc_id,d[word])


if __name__ == '__main__':
   scan_files(config.fragment_file_dir)
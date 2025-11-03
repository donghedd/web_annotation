'''
Author       : Li
Date         : 2020-12-18 18:20:52
LastEditTime : 2021-12-04 13:45:55
LastEditors  :  
Description  : 对文本语料进行预处理，按字级别进行分割；按句子进行切分；处理后的文档，使用utf-8 with bom保存，然后使用excel打开；
FilePath     : /discipline_kg/format_chapter_2_no_blank.py
'''
# -*- coding: utf-8 -*-

# 将每一章的文本数据转换成行模式：
# 1. 每一句话为一行
# 2. 每一行中，将空格等符号删除掉

import numpy as np
import pandas as pd
from pprint import pprint as pp
import logging
from ltp import LTP

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
ltp = LTP()


def get_all_lines(corpus):
    with open(corpus, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    f.close()
    res = ltp.sent_split(lines)
    return res


def filter_sent(corpus):
    # delete the sentences that length is less 2
    meaningful_sentences = []
    res2 = get_all_lines(corpus)
    for idx, len_sent in enumerate(res2):
        # logging.info("ID: {0}, the length of sentence: {1}".format(idx,len(len_sent)))
        if len(len_sent) > 2:
            meaningful_sentences.append(len_sent)
    return meaningful_sentences


def output_format_sentences(corpus, outputName, outputPath):
    res = filter_sent(corpus)
    for idx, sent in enumerate(res):
        split_sent = ltp.sent_split(sent)
        with open(outputPath + outputName, 'a+', encoding='UTF-8') as f:
            f.write(','.join(split_sent) + '\n\n')
    f.close()
    return True


corp10 = 'datasets/corpus_v7/补充语料（期刊和书籍）.txt'
# corp9 = 'datasets/ner_v6/NER_V6.txt'
# corp8 = 'datasets/fourth_corpus/custom_corpus(v4).txt'
# corp7 = 'datasets/cof.txt'
# corp6 = 'datasets/text6.txt'
# corp5 = 'datasets/text5.txt'
# corp4 = 'datasets/text4.txt'
# corp3 = 'datasets/text3.txt'
# corp2 = 'datasets/text2.txt'
# corp1 = 'datasets/text1.txt'
# pathSet = [corp1, corp2, corp3, corp4, corp5, corp6]
pathSet = [corp10]

if __name__ == '__main__':
    for idx, path in enumerate(pathSet):
        output_format_sentences(path,
                                outputPath='datasets/corpus_v7/',
                                outputName='cust_corpus' + str(idx + 1) + '.csv')

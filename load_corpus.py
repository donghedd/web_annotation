# -*- coding: utf-8 -*-
# @Time : 2020/12/21 23:07
# @Author : Lee
# @FileName: load_corpus.py
# @Application_Function:

import pandas as pd
import numpy as np
from pprint import pprint
import configparser

from path_utils import CONFIG_PATH, resolve_path


# to_label_corpus_path = 'labeled_dataset/to_labels_corpus/label_chap1.csv'


def load_sents(path_corpus, limited_lines=5):
    """
    :param path_corpus: 需要标注的语料所在路径
    :param limited_lines: 每一次读取的行数
    :return: 读取的结果
    """
    file_path = resolve_path(path_corpus)
    with file_path.open('r', encoding='utf-8-sig') as f:
        all_sentence = f.readlines()
    all_sentence = all_sentence[0::2]
    return all_sentence[:limited_lines]


# 升级该函数，现在我们每次加载都是从一个语料最初的形态加载，但已经完成标注的句子就不需要加载了
# 改进方案：我们已经给定已完完成标注句子的数目，只需要将这个完成的数字作为加载的初始行标即可
def load_sents2(path_corpus, initial_index, limited_lines=5):
    """
    :param path_corpus: 需要标注的语料所在路径
    :param limited_lines: 每一次读取的行数
    :return: 读取的结果
    """
    file_path = resolve_path(path_corpus)
    with file_path.open('r', encoding='utf-8-sig') as f:
        all_sentence = f.readlines()
    all_sentence = all_sentence[0::2]
    res = all_sentence[initial_index:initial_index + limited_lines]  # 从指定的index开始，提取limited lines行句子
    res2 = []
    # 因为每一句话中可能存在,\n这样的特殊符号，所以下面的程序目的在于删除一句话中的逗号；
    # 这个操作并不会删除中文内容的逗号，因为这个地方过滤,符号是英文状态下的
    for x in res:
        x = [m for m in x if m not in [',', '\n']]
        res2.append(x)
    return res2


#
# test = load_sents2(to_label_corpus_path, 6, 2)
# pprint(test)

# 加载NER类型标签
def load_ners(cfg_file='config.ini', section='GLOBAL'):
    cfg = configparser.ConfigParser()
    cfg_path = resolve_path(cfg_file) if cfg_file != 'config.ini' else CONFIG_PATH
    cfg.read(cfg_path, encoding='utf-8')
    ner_types_path = resolve_path(cfg.get(section, 'ner_types_path', fallback='labeled_dataset/NERs/ner_types.csv'))
    with ner_types_path.open('r', encoding='UTF-8-sig') as f:
        ner_types = f.readlines()
    ners = []
    if ner_types is not None:
        for item in ner_types:
            ners.append(item.strip('\n').split(','))
    return ners


# pprint(load_ners())

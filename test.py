# -*- coding: utf-8 -*-
# @Time : 2020/12/22 14:19
# @Author : Lee
# @FileName: test.py
# @Application_Function:
from load_corpus import load_sents
import logging
from list_current_coupus import list_corpus

def show_corpus(path='label_chap1.csv'):
    res = load_sents(path)
    res2 = []
    for x in res:
        x = [m for m in x if m != ',']
        res2.append(x)
    res2 = res2[:100]
    return res2




print(list_corpus())

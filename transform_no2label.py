# -*- coding: utf-8 -*-
# @Time : 2021/1/7 11:29
# @Author : Lee
# @FileName: transform_no2label.py
# @Application_Function:


# 该函数将web_annotation系统上标注的数字标签，转换成对应的字符标签
# 第一步：读入标签和索引对应的规格文件
# 第二步：将标注中的结果转换成对应的字符标签，插入到一个新列中。

import numpy as np
import pandas as pd

specification = pd.read_csv('labeled_dataset/NERs/ner_types.csv', header=None)

head = specification.iloc[:, 0:2]
head.columns = ['idx', 'labels']
tail = specification.iloc[:, 2:4]
tail.columns = ['idx', 'labels']
new_specification = pd.concat(
    [head, tail]
)
new_specification2 = new_specification.drop_duplicates()


def index2label(raw_label_file, instruction):
    """

    :param raw_label_file: labeled file with numbers
    :param instruction: instruction ner types
    :return: dataframe of labels
    """
    raw_label_file.columns = ['location', 'char', 'idx']

    format_label_res = pd.merge(raw_label_file, instruction.loc[:, ['index', 'labels']], how='left', on='index')
    return format_label_res


raw_labeled_corpus = pd.read_csv('labeled_dataset/labeled_results/merge_labeled_corpus_result.csv', header=None)
raw_labeled_corpus.columns = ['location', 'char', 'idx']

# 合并这行代码有问题，会生成许多错误的标签；
# 经过检查不是方法的错误，而是标注数据中的出现了一个重复标签；
result = raw_labeled_corpus.merge(new_specification2, how='left', on='idx')

print(result)

result.to_excel('new_merge_0414.xlsx', sheet_name='met_book_corpus')

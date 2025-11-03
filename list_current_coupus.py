# -*- coding: utf-8 -*-
# @Time : 2020/12/25 11:25
# @Author : Lee
# @FileName: list_current_coupus.py
# @Application_Function:

# 将该目录下需要标注的语料罗列出来

import os

dir_path = 'labeled_dataset/to_labels_corpus'


def list_corpus(target_path='labeled_dataset/to_labels_corpus'):
    target_directory = target_path

    all_corpus = os.listdir(target_directory)
    target_files_with_path = []
    for file in all_corpus:
        file_path = target_directory + '/' + file
        target_files_with_path.append(file_path)

    return target_files_with_path


def list_chapter_len():
    tmp = list_corpus()
    file_dict = {}
    for file in tmp:
        with open(file, 'r') as f:
            tmp_file = f.readlines()
        len_file = len(tmp_file)
        file_dict[file] = len_file
        res_dict = sorted(file_dict.items(), key=lambda item: item[0]) #对结果字典进行排序
    return dict(res_dict)


# -*- coding: utf-8 -*-
# @Time : 2020/12/23 13:25
# @Author : Lee
# @FileName: json_format.py
# @Application_Function:
# 这个程序是将收到的json数据转换成对应的句子、对应文字，对应标签的数据格式
# 并将上述转换的结构写入到新的文件中

import json
import logging
from pathlib import Path
from typing import Union

import pandas as pd

from path_utils import ensure_directory, resolve_path


# output_path = 'labeled_dataset/labeled_results/'
# output_file_name = 'chap1.csv'
# inputFile = 'labeled_dataset/chap11.json'


def check_file_exist(readFile: Union[str, Path]):
    '''
    :param readFile: 输入需要读入的文件地址，路径+文件名
    :return: boolean
    该函数判断输入的文件名是否存在
    '''
    return resolve_path(readFile).exists()


def format_json_to_dataFrame(outpath: Union[str, Path], fileName: str, readFile: Union[str, Path]):
    """
    :param path: output path , which is a directory path
    :param fileName: identify the target file name
    :param readFile:  identify input file, which should a json file
    :return: boolean
    这个程序是通过前台标注后，提交传过来的一个json文件，将这个json文件转换成目标的dataFrame格式，并输出
    """
    if check_file_exist(readFile):
        input_path = resolve_path(readFile)
        with input_path.open('r', encoding='utf-8') as js:
            res = json.load(js)
        res.pop('csrf_token', None)  # 删除表单提交后，网页自带的csrf_token行内容；
        res_list = list(res)
        # step1 删除空白，未标注的单词
        sentences = res_list[::2]  # 筛选出句子标识符
        words_id = res_list[1::2]  # 筛选出文字对应的标识符
        words_name = [res[x] for x in words_id]  # 获取对应的文字名称
        words_labels = [res[x] for x in sentences]  # 获取文字对应的标签数字符号

        # 构造成表格形式DataFrame
        new_labeled_data = pd.DataFrame({
            'sent_id': sentences,
            'words_name': words_name,
            'words_labels': words_labels
        })
        # filter_labeled_sentences = new_labeled_data[new_labeled_data['words_labels'] != '']  # 筛选出仅完成标注的那些句子和字符； 更新：不需要筛选，因为后期训练的时候，标点符号也需要纳入考虑；
        output_dir = ensure_directory(outpath)
        output_file = output_dir / fileName
        new_labeled_data.to_csv(output_file, mode='a+', index=False, header=False)
        return True
    else:
        logging.info('Files are not found!')
        return False

# print(format_json_to_dataFrame(output_path,output_file_name,inputFile))

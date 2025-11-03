# -*- coding: utf-8 -*-
# @Time : 2020/12/27 12:57
# @Author : Lee
# @FileName: reset_to_initial.py
# @Application_Function:

# This function is to be used for reset all system to the initial, which includes three parts:
#     1. delete all files in directory "labeled_results"
#     2. delete all files in directory "raw_labeled_data_from_web"
#     3. reset the parameter "INITIAL" in config.ini file
#  该函数仅限管理员操作

import configparser
import os
import shutil
import time
import sys


def reset_config(config_path):
    cfg = configparser.ConfigParser()
    cfg.read(config_path)
    for key, value in cfg['INITIAL'].items():
        cfg['INITIAL'][key] = str(0)
    cfg.write(open(config_path, 'w'))
    return True


def reset_app(config_path='/Users/lee/Documents/code_project/flask_web_annotation/config.ini'):
    cfg = configparser.ConfigParser()
    cfg.read(config_path)
    backup_file_name = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    backup_dir = cfg.get('BACKUP', 'backup_dir_path')
    target_dir_path = cfg.get('BACKUP', 'data_dir_path')
    if os.listdir(target_dir_path):
        bk = shutil.make_archive(backup_dir + backup_file_name, 'gztar', root_dir=target_dir_path)
        if bk:
            shutil.rmtree(target_dir_path)  # 晒出目标目录下的文件
            os.mkdir(target_dir_path)
            reset_config(config_path)
    else:
        reset_config(config_path)
    return True


# reset_app() 此方法会调用该函数将目前的程序恢复到初始状态，务必谨慎操作！

if __name__ == '__main__':
    path = sys.argv[1]
    reset_app(config_path=path)

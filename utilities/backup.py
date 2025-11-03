# -*- coding: utf-8 -*-
# @Time : 2020/12/27 13:45
# @Author : Lee
# @FileName: backup.py
# @Application_Function:
# 该函数实现定时对目标文件下的内容进行备份操作

import os
import shutil
import time
import configparser


def backup(config_path='/Users/lee/Documents/code_project/flask_web_annotation/config.ini'):
    cfg = configparser.ConfigParser()
    cfg.read(config_path)
    backup_file_name = 'bk_files_' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    backup_dir = cfg.get('BACKUP', 'backup_dir_path')
    target_dir_path = cfg.get('BACKUP', 'data_dir_path')
    res = shutil.make_archive(backup_dir+backup_file_name, 'gztar', target_dir_path)
    return True


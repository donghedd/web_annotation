# -*- coding: utf-8 -*-
# @Time : 2020/12/26 17:29
# @Author : Lee
# @FileName: update_config.py
# @Application_Function:

# 该函数处理与更新config配置文件相关的操作
import configparser


def update_config(item, value, cfg_file='config.ini', section='INITIAL'):
    cfg = configparser.ConfigParser()
    cfg.read(cfg_file)
    if section in cfg.sections() and item in cfg[section].keys():
        cfg.set(section, item, str(value))
        cfg.write(open(cfg_file, 'w'))
        return True
    else:
        return "section or item is not exist!"


def update_config_keys(keysets, cfg_file='config.ini', section='INITIAL'):
    cfg = configparser.ConfigParser()
    cfg.read(cfg_file)
    if section in cfg.sections():
        cfg_dict = dict(cfg[section])
        origin_keys = cfg_dict.keys()
        new_cfg_dict = {}
        for item, origin_key in zip(keysets, origin_keys):
            # print(item + 'vs' + origin_key) # 调试输出之用
            new_cfg_dict[item] = cfg_dict[origin_key]
            cfg[section] = new_cfg_dict
            cfg.write(open(cfg_file, 'w'))
        return True
    else:
        return "section is not exist!"


def check_login(accountName, password):
    username = accountName
    pwd = password
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')
    account_index_of_sections = cfg.getint('ACCOUNT', 'START_INDEX_OF_SECTIONS')
    accounts = cfg.sections()[account_index_of_sections:]  # 3表示账户开始设定的第一个section
    dict_account = {}
    for acct in accounts:
        dict_account[dict(cfg[acct])['username']] = dict(cfg[acct])['pwd']
    if username in dict_account.keys() and pwd == dict_account[username]:
        return True
    else:
        return False

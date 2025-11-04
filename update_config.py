# -*- coding: utf-8 -*-
# @Time : 2020/12/26 17:29
# @Author : Lee
# @FileName: update_config.py
# @Application_Function:

# 该函数处理与更新config配置文件相关的操作
import configparser

from path_utils import CONFIG_PATH, resolve_path


def _resolve_config(cfg_file: str):
    if cfg_file == 'config.ini':
        return CONFIG_PATH
    return resolve_path(cfg_file)


def update_config(item, value, cfg_file='config.ini', section='INITIAL'):
    cfg = configparser.ConfigParser()
    cfg_path = _resolve_config(cfg_file)
    cfg.read(cfg_path, encoding='utf-8')
    if section in cfg.sections() and item in cfg[section].keys():
        cfg.set(section, item, str(value))
        with cfg_path.open('w', encoding='utf-8') as config_stream:
            cfg.write(config_stream)
        return True
    else:
        return "section or item is not exist!"


def update_config_keys(keysets, cfg_file='config.ini', section='INITIAL'):
    cfg = configparser.ConfigParser()
    cfg_path = _resolve_config(cfg_file)
    cfg.read(cfg_path, encoding='utf-8')
    if section in cfg.sections():
        cfg_dict = dict(cfg[section])
        origin_keys = cfg_dict.keys()
        new_cfg_dict = {}
        for item, origin_key in zip(keysets, origin_keys):
            # print(item + 'vs' + origin_key) # 调试输出之用
            new_cfg_dict[item] = cfg_dict[origin_key]
            cfg[section] = new_cfg_dict
            with cfg_path.open('w', encoding='utf-8') as config_stream:
                cfg.write(config_stream)
        return True
    else:
        return "section is not exist!"


def check_login(accountName, password):
    username = accountName
    pwd = password
    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_PATH, encoding='utf-8')
    try:
        account_index_of_sections = cfg.getint('ACCOUNT', 'START_INDEX_OF_SECTIONS')
    except (configparser.NoOptionError, configparser.NoSectionError, ValueError):
        account_index_of_sections = None

    sections = cfg.sections()
    if account_index_of_sections is not None and account_index_of_sections < len(sections):
        account_sections = sections[account_index_of_sections:]
    else:
        account_sections = [
            section for section in sections
            if section.lower().startswith('account') and section.lower() != 'account'
        ]

    dict_account = {}
    for acct in account_sections:
        section_dict = dict(cfg[acct])
        acct_username = section_dict.get('username')
        acct_pwd = section_dict.get('pwd')
        if not acct_username or acct_pwd is None:
            continue
        dict_account[acct_username] = acct_pwd

    return username in dict_account and pwd == dict_account[username]

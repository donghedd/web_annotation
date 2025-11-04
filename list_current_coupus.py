# -*- coding: utf-8 -*-
# @Time : 2020/12/25 11:25
# @Author : Lee
# @FileName: list_current_coupus.py
# @Application_Function:

# 将该目录下需要标注的语料罗列出来

import configparser
import logging
from typing import Dict, List, Optional

from path_utils import CONFIG_PATH, as_config_path, resolve_path

LOGGER = logging.getLogger(__name__)

DEFAULT_CORPUS_DIR = "labeled_dataset/to_labels_corpus"


def _get_corpus_dir() -> str:
    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_PATH, encoding="utf-8")
    return cfg.get("PATHS", "to_labels_dir", fallback=DEFAULT_CORPUS_DIR)


def list_corpus(target_path: Optional[str] = None) -> List[str]:
    corpus_dir = target_path or _get_corpus_dir()
    resolved_dir = resolve_path(corpus_dir)

    if not resolved_dir.exists():
        LOGGER.warning("Corpus directory not found: %s", resolved_dir)
        return []

    target_files_with_path: List[str] = []
    for file in sorted(resolved_dir.iterdir()):
        if file.is_file():
            target_files_with_path.append(as_config_path(file))

    return target_files_with_path


def list_chapter_len() -> Dict[str, int]:
    tmp = list_corpus()
    file_dict: Dict[str, int] = {}
    for file in tmp:
        file_path = resolve_path(file)
        if not file_path.exists():
            LOGGER.warning("Corpus file missing: %s", file_path)
            continue
        with file_path.open("r", encoding="utf-8-sig") as f:
            tmp_file = f.readlines()
        len_file = len(tmp_file)
        file_dict[file] = len_file
    res_dict = sorted(file_dict.items(), key=lambda item: item[0])  # 对结果字典进行排序
    return dict(res_dict)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import shutil
import traceback
import hashlib
import os
from urllib import parse
import yaml
import logging

logger = logging


# 方法调用日志
def func_result_logger(func_result_info=False, message=""):
    def decorator(func):
        def wrapper(*args, **kw):
            try:
                func_from = traceback.extract_stack()
                result = func(*args, **kw)
                if func_result_info:
                    info = f"{message}\n" \
                           f"执行方法路径:{str(func_from)}\n" \
                           f"结果{str(result)}"
                    print(info)
                    logger.info(info)
            except Exception as e:
                logger.error(e)
                result = False
            return result

        return wrapper

    return decorator


# url解析
def url_parse(url):
    scheme, netloc, path, params, query, fragment = parse.urlparse(url)
    if scheme == "" or netloc == "" or path in "":
        return False
    else:
        return {"host": netloc, "path": path, "scheme": scheme}


def md5(data):
    m = hashlib.md5()
    m.update(data.encode('utf-8'))
    MD5 = m.hexdigest()
    return MD5


def get_response_content_md5(response_content):
    md5_obj = hashlib.md5()
    md5_obj.update(response_content)
    hash_code = md5_obj.hexdigest()
    md5 = str(hash_code).lower()
    return md5


def make_dir(path):
    if os.path.exists(path) is False:
        os.mkdir(path)


def get_file_yaml_list(path, result=None):
    if result is None:
        result = []
    for root, dirs, files in os.walk(path):
        temp_yaml_list = []
        for file in files:
            if (file.endswith(".yml") or file.endswith(".yaml")) and file.startswith("!") is False:
                temp_yaml_list.append(os.path.abspath(root + "/" + file))
        result += temp_yaml_list
        [get_file_yaml_list(dir, result) for dir in dirs]
    return result


def get_yaml_case(path):
    if os.path.isdir(path):
        file_path_list = get_file_yaml_list(path)
    else:
        if path.endswith(".yml") or path.endswith(".yaml"):
            file_path_list = [path]
        else:
            file_path_list = []
    return [yaml.safe_load(open(file_path)) for file_path in file_path_list]


def del_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path=path)


def del_file(path):
    if os.path.exists(path):
        os.remove(path=path)

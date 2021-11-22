#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import time
from typing import List

from sanic.log import logger
import traceback
import hashlib
import os
from urllib import parse
import yaml
import datetime
import pytz


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


def params_jira_keys(keys: List[str]):
    result = []
    for key in keys:
        if key:
            try:
                result.append(key.split('/')[-1].strip(' '))
            except Exception as e:
                print(e)
                return []
    return result


def utc_time_to_timestamp(date_time_str):
    os.environ['TZ'] = "UTC"
    try:
        date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        timestamp = date_time_obj.timestamp()
    except Exception as e:
        timestamp = False
    del os.environ['TZ']
    return timestamp


def utc_8_time_to_timestamp(date_time_str):
    os.environ['TZ'] = "UTC"
    try:
        date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        timestamp = date_time_obj.timestamp() - 3600 * 8
    except Exception as e:
        timestamp = False
    del os.environ['TZ']
    return timestamp


def tran_objLevel_to_strLevel(level):
    levels = ['levelOne', 'levelTwo', 'levelThree']
    return ','.join([level.get(key) for key in levels if level.get(key)])

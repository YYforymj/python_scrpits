# -*- coding: utf-8 -*-
"""
Author: BigCat
"""
import os

URL = "https://datachart.500.com/ssq/history/"
path = "newinc/history.php?start={}&end="

BOLL_NAME = [
    ("红球", "red"),
    ("蓝球", "blue")
]

# 日志路径
log_path = os.getcwd() + "/log/"
access_log = log_path + "access.log"
error_log = log_path + "error.log"

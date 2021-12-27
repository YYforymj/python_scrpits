# -*- coding:utf-8 -*-
"""
Author: BigCat
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup

import send_mail
from config import *

target1 = pd.Series()
target1[u"红球号码_1"] = '05'
target1[u"红球号码_2"] = '09'
target1[u"红球号码_3"] = '10'
target1[u"红球号码_4"] = '13'
target1[u"红球号码_5"] = '21'
target1[u"红球号码_6"] = '27'
target1[u"蓝球"] = '12'

test = pd.Series()
test[u"红球号码_1"] = '04'
test[u"红球号码_2"] = '07'
test[u"红球号码_3"] = '17'
test[u"红球号码_4"] = '13'
test[u"红球号码_5"] = '21'
test[u"红球号码_6"] = '24'
test[u"蓝球"] = '16'


def get_current_number():
    """ 获取最新一期数字
    :return: int
    """
    r = requests.get("{}{}".format(URL, "history.shtml"))
    r.encoding = "gb2312"
    soup = BeautifulSoup(r.text, "lxml")
    current_num = soup.find("div", class_="wrap_datachart").find("input", id="end")["value"]
    return current_num


def spider(start, end, mode):
    """ 爬取历史数据
    :param start 开始一期
    :param end 最近一期
    :param mode 模式
    :return:
    """
    url = "{}{}{}".format(URL, path.format(start), end)
    r = requests.get(url=url)
    r.encoding = "gb2312"
    soup = BeautifulSoup(r.text, "lxml")
    trs = soup.find("tbody", attrs={"id": "tdata"}).find_all("tr")
    for tr in trs:
        item = pd.Series()
        serial_num = tr.find_all("td")[0].get_text().strip()
        item[u"红球号码_1"] = tr.find_all("td")[1].get_text().strip()
        item[u"红球号码_2"] = tr.find_all("td")[2].get_text().strip()
        item[u"红球号码_3"] = tr.find_all("td")[3].get_text().strip()
        item[u"红球号码_4"] = tr.find_all("td")[4].get_text().strip()
        item[u"红球号码_5"] = tr.find_all("td")[5].get_text().strip()
        item[u"红球号码_6"] = tr.find_all("td")[6].get_text().strip()
        item[u"蓝球"] = tr.find_all("td")[7].get_text().strip()
        return item, serial_num


def match_red(balls1, balls2):
    i = 1
    j = 1
    match = []
    while i <= 6 and j <= 6:
        if balls1['红球号码_' + str(i)] == balls2['红球号码_' + str(j)]:
            match.append(balls1['红球号码_' + str(i)])
            i = i + 1
            j = j + 1
            continue
        if int(balls1['红球号码_' + str(i)]) > int(balls2['红球号码_' + str(j)]):
            j = j + 1
            continue
        if int(balls1['红球号码_' + str(i)]) < int(balls2['红球号码_' + str(j)]):
            i = i + 1
            continue
    return match


def match_blue(balls1, balls2):
    if balls1[u"蓝球"] == balls2[u"蓝球"]:
        return True
    else:
        return False


def get_award_level(balls1, balls2):
    match = match_red(balls1, balls2)
    red_length = match.__len__()
    blue_match = match_blue(balls1, balls2)
    if red_length == 6 and blue_match:
        return 1
    if red_length == 6 and not blue_match:
        return 2
    if red_length == 5 and blue_match:
        return 3
    if (red_length == 5 and not blue_match) or (red_length == 4 and blue_match):
        return 4
    if (red_length == 4 and not blue_match) or (red_length == 3 and blue_match):
        return 5
    if (red_length == 2 and blue_match) or (red_length == 0 and blue_match) \
            or (red_length == 0 and blue_match):
        return 6
    return 0


if __name__ == "__main__":
    # print("[INFO] 最新一期期号：{}".format(get_current_number()))
    # print("[INFO] 正在获取数据。。。")
    if not os.path.exists(train_data_path):
        os.mkdir(train_data_path)
    pd, serial_num = spider(get_current_number(), get_current_number(), "predict")
    # print("[INFO] 数据获取完成，{}", pd)
    award_level = get_award_level(pd, target1)
    # print(award_level)
    if award_level > 0:
        msg = "中奖了，{}等奖".format(award_level)
    else:
        msg = "未中奖"
    msg = msg + "\r\n<br\>开奖期次：{}".format(serial_num)
    msg = msg + "\r\n<br\>预留号码：{}, \r\n<br\>本期中奖号码：{}".format(target1.values, pd.values)
    print(msg)
    send_mail.send_mail(msg)

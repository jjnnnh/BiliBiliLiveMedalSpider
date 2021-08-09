#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import re
import time


def getMedal(roomid):    # 与getHTML()函数合并，直接获取勋章
    try:
        url = 'https://live.bilibili.com/' + str(roomid)  # 直播间url
        headers = {'user-agent': 'Chrome/83'}  # 伪造请求头
        html = requests.get(url, headers=headers)  # 提交请求，并获得响应
        html.encoding = 'utf-8'  # b站直播采用utf-8编码
        html.raise_for_status  # 如果状态码不为200即爬取失败则产生异常
        html = html.text  # 返回网页HTML
        match = regex_medal.findall(html)  # 通过正则表达式匹配查询结果，获取粉丝勋章名称
        if len(match):  # 如果该直播间开通了粉丝勋章
            return match[0]  # 返回获取粉丝勋章名称
        else:
            return ''  # 否则返回空字符串
    except:# 异常处理
        with open('err.txt', 'a', encoding='utf-8') as logfile:# 在"err.txt"中添加错误记录
            print('房间' + str(roomid) + '爬取失败', file=logfile)

# 程序入口
regex_medal = re.compile(r'(?<="medal_name":")[^"]*')  # 用于匹配粉丝勋章的正则表达式
with open('settings.json', 'r') as f:  # 读取配置文件
    settings = json.load(f)
    num1 = settings['num1']
    num2 = settings['num2']
# 初始化相关参数
num = num2 - num1 + 1  # 爬取的房间总数
num_percent = max(num // 10000, 1)  # 用于显示进度的基数
with open('log.txt', 'w', encoding='utf-8') as logfile:  # 清空"log.txt"
    print('爬取开始', file=logfile)
with open('medal.txt', 'w', encoding='utf-8') as medalfile:  # 清空"medal.txt"
    print('勋章字典：', file=medalfile)
with open('medalfst.txt', 'w', encoding='utf-8') as medalfstfile:  # 清空"medalfst.txt"
    print('勋章粉丝团：', file=medalfstfile)
for i in range(num1, num2):  # 遍历直播间
    # 原getRuid()函数变更为getMedal()直接获取粉丝勋章
    medalname = getMedal(i)
    if medalname:
        # 判断默认粉丝勋章"粉丝团"
        if medalname == "粉丝团":
            WJ = "medalfst.txt"
            XR = i
        else:
            WJ = "medal.txt"
            XR = '{}:{}'.format(medalname, i)
        with open(WJ, 'a', encoding='utf-8') as medalfile:  # 以追加模式按需打开文件，注意编码格式
            print(XR,
                  file=medalfile)  # 按需写入
    if i % num_percent == 0:  # 显示进度
        with open('log.txt', 'w', encoding='utf-8') as logfile:  # 以写入模式打开"log.txt"
            print('{} {}/{} {:.2f}% compelete'.format(time.ctime(),
                                                      i - num1 + 1, num, i * 100 / num), file=logfile)  # 输出当前时间、进度，增强用户体验
with open('log.txt', 'a', encoding='utf-8') as logfile:
    print('爬取结束', file=logfile)  # 爬取完毕，输出提示信息

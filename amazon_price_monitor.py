#!/usr/bin/env python
# coding: utf-8
# @Author : JackLee 
# @contact: jackleeforce@gmail.com
# @Time : 2019-06-10 15:56 
# @File : amazon_price_monitor.py 
# @desc:
import logging

import func


def init_log():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s-%(name)s-%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    # 使用FileHandler输出到文件
    fh = logging.FileHandler('amazon_price_monitor.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    # 使用StreamHandler输出到屏幕
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)



if __name__ == "__main__":
    init_log()

    func.init_ssl()

    exit(0)
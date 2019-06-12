#!/usr/bin/env python
# coding: utf-8
# @Author : JackLee
# @contact: jackleeforce@gmail.com
# @Time : 2019-06-10 15:56
# @File : amazon_china_price_monitor.py
# @desc:
import logging
import time
from urllib.parse import urlparse

import requests
from lxml import etree
from user_agent import generate_user_agent

import func
from wechatsender import WeChatSender

corpid = 'ww8d16902788f36764'
corpsecret = 'u7hTPhjrtxY4yRO3LJ6SRDdfgWbP1-n-XtHBGKE7DMw'
agentid = '1000003'


def shrink_price(str_price):
    new_price = str_price.replace('￥', '')
    new_price = new_price.replace(',', '')

    return float(new_price)


def monitor_amazon_china():
    monitor_targets = [
        {'url': 'https://www.amazon.cn/dp/B07CRZK9BX', 'ideal_price': 900.00, 'lowst_price_history': 0.00,
         'last_notify_date': ''},
        {'url': 'https://www.amazon.cn/dp/B07G3QMPB5', 'ideal_price': 900.00, 'lowst_price_history': 0.00,
         'last_notify_date': ''},
        {'url': 'https://www.amazon.cn/dp/B07CMH78R5', 'ideal_price': 900.00, 'lowst_price_history': 0.00,
         'last_notify_date': ''}]

    session = requests.session()

    for monitor_target in monitor_targets:
        target_url = monitor_target.get('url')
        ideal_price = monitor_target.get('ideal_price')
        lowst_price_history = monitor_target.get('lowst_price_history')
        last_notify__date = monitor_target.get('last_notify_date')

        o = urlparse(target_url)
        ref = o.scheme + '://' + o.hostname
        ua = generate_user_agent()
        session.headers['User-Agent'] = ua
        session.headers['referer'] = ref

        response = session.get(target_url)

        response.raise_for_status()

        html_source = response.text

        selector = etree.HTML(html_source)

        title = (selector.xpath('//span[@id="productTitle"]/text()')[0]).strip()
        current_price = selector.xpath('//span[@id="priceblock_ourprice"]/text()')[0]
        current_float_price = shrink_price(current_price)

        logging.debug(title + ',' + current_price + ',url:' + target_url)

        if current_float_price <= ideal_price:
            current_date = time.strftime("%Y-%m-%d", time.localtime())

            if current_date != last_notify__date:
                monitor_target['last_notify_date'] = current_date

                message = 'Item name:{0} \nurl:{1}\nreached your ideal price:\n{2}\ncurrent price:\n{3}\n'.format(title,
                                                                                                                  target_url,
                                                                                                                  ideal_price,
                                                                                                                  current_float_price)

                if lowst_price_history == 0.00 or current_float_price <= lowst_price_history:
                    monitor_target['lowst_price_history'] = current_price
                    message += 'This price is the lowst price in the history'

                logging.debug(message)

                wechat_sender = WeChatSender(corpid, corpsecret, agentid)

                wechat_sender.send_text_msg(message)


if __name__ == '__main__':
    func.init_ssl()

    func.init_log('price_monitor.log')

    wechat_sender = WeChatSender(corpid, corpsecret, agentid)

    wechat_sender.send_text_msg('Start to monitor amazon china bug price')

    retryCount = 0

    while True:
        error_occured = False
        try:
            monitor_amazon_china()
        except Exception as e:
            logging.exception(e)
            logging.error('Something wrong,retry count:' + retryCount)
            wechat_sender.send_text_msg('Something wrong,retry count:' + retryCount)
            retryCount += 1
            error_occured = True

        if not error_occured:
            retryCount = 0
        elif retryCount >= 3:
            wechat_sender.send_text_msg('Something wrong,quit job')
            break

        time.sleep(60)

    exit(0)

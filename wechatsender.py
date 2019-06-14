#!/usr/bin/env python
# coding: utf-8
# @Author : JackLee 
# @contact: jackleeforce@gmail.com
# @Time : 2019-06-03 15:04 
# @File : wechatsender.py
# @desc:
import json
import logging

import requests

error_code_successful = 0
error_code_busy = -1
error_code_invalid_access_token = 40014
error_code_access_token_expired = 42001


class WeChatSender:
    __session = requests.session()
    __access_token = None

    def __init__(self, corp_id, corp_secret, agent_id):
        self.corp_id = corp_id
        self.corp_secrect = corp_secret
        self.agent_id = agent_id

        self.__obtain_access_token()

    # 获取 access token
    def __obtain_access_token(self):

        self.__access_token = None

        try:

            url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={0}&corpsecret={1}".format(self.corp_id,
                                                                                                  self.corp_secrect)
            response = self.__session.get(url)

            response.raise_for_status()

            logging.debug("__obtain_access_token response:" + response.text)

            if response.status_code == 200:
                self.__access_token = json.loads(response.content)['access_token']
            else:
                logging.exception("__obtain_access_token response code not 200.")
        except Exception as e:
            logging.exception(e)

    # 发送文本消息。
    def send_text_msg(self, msg):
        max_retry_count = 3
        retry_count = 0

        header = {
            "Content-Type": "application/json"
        }
        form_data = {
            "touser": "@all",
            "toparty": "",
            "totag": "",
            "msgtype": "text",
            "agentid": self.agent_id,
            "text": {
                "content": msg
            },
            "safe": 0
        }

        while retry_count < max_retry_count:
            if self.__access_token is None:
                self.__obtain_access_token()

            url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.__access_token

            try:
                response = self.__session.post(url, data=json.dumps(form_data).encode('utf-8'), headers=header)

                logging.debug("send_text_msg response:" + response.text)

                if response.status_code == 200:
                    error_code = json.loads(response.content)['errcode']

                    if error_code == error_code_invalid_access_token or error_code == error_code_access_token_expired:
                        self.__access_token = None
                        retry_count += 1
                    elif error_code == error_code_busy:
                        retry_count += 1
                    elif error_code != error_code_successful:
                        logging.exception("send_text_msg response error_code not 0.")
                        return -1
                    else:
                        return 0

                else:
                    logging.exception("send_text_msg response code not 200.")
                    retry_count += 1
            except Exception as e:
                logging.exception(e)
                retry_count += 1

        return 0

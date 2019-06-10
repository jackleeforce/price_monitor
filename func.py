# -*- coding: utf-8 -*-
import logging
import os
import ssl
import time
import urllib.error
import urllib.request
from urllib.parse import urlparse

from user_agent import generate_user_agent


def init_ssl():
    ssl._create_default_https_context = ssl._create_unverified_context


def create_folder(dir):
    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok=True)


def download_image(image_url, download_dir, name):
    headers = {}

    try:
        o = urlparse(image_url)
        ref = o.scheme + '://' + o.hostname
        ua = generate_user_agent()
        headers['User-Agent'] = ua
        headers['referer'] = ref

        req = urllib.request.Request(image_url.strip(), headers=headers)
        response = urllib.request.urlopen(req)

        data = response.read()
        file_path = download_dir + '{0}.jpg'.format(name)
        with open(file_path, 'wb') as wf:
            wf.write(data)

    except Exception as e:
        logging.exception(e)

#!usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: EarlGrey@codingpy.com
# Copyright: Public Domain
#

import time
import requests

import oss2
from qcloud_cos import StatFileRequest
from qcloud_cos import CosClient


def download_oss(file):
    access_key = '# 根据自己的情况填写'
    access_secret = '# 根据自己的情况填写'
    auth = oss2.Auth(access_key, access_secret)
    endpoint = '# 根据自己的情况填写'
    bucket = oss2.Bucket(auth, endpoint, '# 根据自己的情况填写')
    download_url = bucket.sign_url('GET', file, 60)

    start = time.time()
    r = requests.get(download_url, timeout=60)
    end = time.time()
    if r.status_code != 200:
        return 0
    elapsed = (end - start) * 1000.0

    print 'OSS Download File Time %0.3f ms' % elapsed
    return elapsed


def download_cos(file):
    appid = 100000  # 根据自己的情况填写
    secret_id = u'# 根据自己的情况填写'
    secret_key = u'# 根据自己的情况填写'
    region = '# 根据自己的情况填写'
    bucket = u'# 根据自己的情况填写'

    cos_client = CosClient(appid, secret_id, secret_key, region)
    request = StatFileRequest(bucket, u'/' + file)
    stat = cos_client.stat_file(request)
    if stat['code'] != 0:
        return 0
    download_url = stat['data']['source_url']  # 使用外网直接访问 URL

    start = time.time()
    r = requests.get(download_url, timeout=60)
    end = time.time()
    if r.status_code != 200:
        return 0
    elapsed = (end - start) * 1000.0

    print 'COS Download File Time %0.3f ms' % elapsed
    return elapsed

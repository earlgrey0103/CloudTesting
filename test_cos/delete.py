#!usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: EarlGrey@codingpy.com
# Copyright: Public Domain
#

import time

import oss2
from qcloud_cos import CosClient, DelFileRequest


def delete_oss(file):
    access_key = '# 根据自己的情况填写'
    access_secret = '# 根据自己的情况填写'
    auth = oss2.Auth(access_key, access_secret)
    endpoint = '# 根据自己的情况填写'
    bucket = oss2.Bucket(auth, endpoint, '# 根据自己的情况填写')

    start = time.time()
    resp = bucket.delete_object(file)
    end = time.time()
    if resp.status != 204:
        return 0
    elapsed = (end - start) * 1000.0

    print 'OSS Delete File Time %0.3f ms' % elapsed
    return elapsed


def delete_cos(file):
    appid = 10000  # 根据自己的情况填写
    secret_id = u'# 根据自己的情况填写'
    secret_key = u'# 根据自己的情况填写'
    region = '# 根据自己的情况填写'
    bucket = u'# 根据自己的情况填写'

    cos_client = CosClient(appid, secret_id, secret_key, region)
    cos_path = u'/' + file

    request = DelFileRequest(bucket, cos_path)

    start = time.time()
    resp = cos_client.del_file(request)
    # assert resp['code'] == 0
    end = time.time()
    if resp['code'] != 0:
        return 0
    elapsed = (end - start) * 1000.0
    print 'COS Delete File Time %0.3f ms' % elapsed
    return elapsed

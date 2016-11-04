#!usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: EarlGrey@codingpy.com
# Copyright: Public Domain
#

import time

import oss2
from qcloud_cos import CosClient, UploadFileRequest


def upload_oss(file):
    access_key = '# 根据自己的情况填写'
    access_secret = '# 根据自己的情况填写'
    auth = oss2.Auth(access_key, access_secret)
    endpoint = '# 根据自己的情况填写'
    bucket = oss2.Bucket(auth, endpoint, '# 根据自己的情况填写')
    with open(file, 'rb') as fileobj:
        start = time.time()
        resp = bucket.put_object(file, fileobj)
        end = time.time()
        if resp.status != 200:
            return 0
        elapsed = (end - start)*1000.0
        print u'本次 OSS 文件上传时间为 %0.3f ms' % elapsed
    return elapsed


def upload_cos(file):
    """
    CVM 上报 https 错误：取消 https 试试
    """
    appid = 100000  # 根据自己的情况填写
    secret_id = u'# 根据自己的情况填写'
    secret_key = u'# 根据自己的情况填写'
    region = '# 根据自己的情况填写'
    bucket = u'# 根据自己的情况填写'

    cos_client = CosClient(appid, secret_id, secret_key, region)

    cos_path = u'/' + file

    request = UploadFileRequest(bucket, cos_path, unicode(file))
    request.set_insert_only(0)

    start = time.time()
    resp = cos_client.upload_file(request)
    # assert resp['code'] == 0
    if resp['code'] != 0:
        return 0
    end = time.time()

    elapsed = (end - start)*1000.0

    print u'本次 COS 文件上传时间为 %0.3f ms' % elapsed

    return elapsed

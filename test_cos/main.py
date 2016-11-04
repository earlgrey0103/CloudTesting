#!usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: EarlGrey@codingpy.com
# Copyright: Public Domain
#

import os
import csv
import time
import sys
import subprocess

from upload import upload_oss, upload_cos
from download import download_oss, download_cos
from delete import delete_oss, delete_cos

from utils import get_filenames, write_to_csv


def setup(size):
    subprocess.call(['make', 'setup_%s' % size])


def cleanup(size):
    subprocess.call(['rm', '-rf', '%s/' % size])


def test_suite(size='50k', method='upload', provider='cos'):

    methods = {
        'oss': {
            'upload': upload_oss,
            'download': download_oss,
            'delete': delete_oss,
        },
        'cos': {
            'upload': upload_cos,
            'download': download_cos,
            'delete': delete_cos,
        }
    }

    data = {
        provider: [],
    }

    filenames = get_filenames('%s' % size)
    num = 0

    for file in filenames:
        elapsed = methods[provider][method](file)
        if elapsed != 0:
            data[provider].append(elapsed)
            num += 1

    for item in data:
        total = float(sum(data[item]))
        avg = total / max(num, 1)
        print '%s: total %s for %s files is:  %0.3f ms' % (item, method, size, total)
        print '%s: average %s for %s files is:  %0.3f ms' % (item, method, size, avg)

    csv_file = 'test_%s_%s_%s.csv' % (size, method, provider)
    write_to_csv(data, csv_file)

    final_csv = 'final_%s_%s_%s.csv' % (size, method, provider)
    with open(final_csv, 'w') as f:
        w = csv.writer(f)
        w.writerow(['平均值', '总数'])
        w.writerow([avg, total])


if __name__ == '__main__':
    methods = ['upload', 'download', 'delete']
    provider, size = sys.argv[1], sys.argv[2]

    for method in methods:
        test_suite(size, method, provider)

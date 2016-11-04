#!usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: EarlGrey@codingpy.com
# Copyright: Public Domain
#

import os
import csv


def get_filenames(path):
    for root, directories, filenames in os.walk(path):
        for filename in filenames:
            if '.DS_Store' not in filename:
                yield os.path.join(root, filename)



def get_directories(path):
    res = []
    for root, directories, filenames in os.walk(path):
        for directory in directories:
            res.append(os.path.join(root, directory))
    return res


def write_to_csv(data, file):
    """
    Data: dictionary
    """
    with open(file, 'wb') as f:
        w = csv.writer(f)
        w.writerow(data.keys())
        w.writerows(zip(*data.values()))

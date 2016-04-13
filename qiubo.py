#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import time
import sys
from qiubo_student import QiuBoStudent

def main():
    if len(sys.argv) == 1:
        try:
            with open('qiubo.json', 'r') as config_file:
                config = json.load(config_file)
        except:
            print('Failed to load configuration file qiubo.json!')
            exit()
    else:
        config = {
            'id': sys.argv[1],
            'sign_in_log': True
        }

    while 1:
        try:
            student = QiuBoStudent(config['id'])
            break
        except requests.exceptions.RequestException:
            print(u'网络连接失败')
            time.sleep(3)

    while 1:
        try:
            student.wait_for_next_course()
            student.sign_in(log=config['sign_in_log'])
            time.sleep(3900)
        except requests.exceptions.RequestException:
            print(u'网络连接失败！')
            time.sleep(3)

if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import time
from qiubo_student import QiuBoStudent

def main():
    config = {}

    try:
        with open('qiubo.json', 'r') as config_file:
            config = json.load(config_file)
    except:
        print('Failed to load configuration file qiubo.json!')
        exit()

    while 1:
        try:
            student = QiuBoStudent(config['id'])
            # student.print_schedule()
            break
        except requests.exceptions.RequestException:
            print(u'网络连接失败')
            time.sleep(5)

    while 1:
        try:
            student.wait_for_next_course()
            student.sign_in(log=config['sign_in_log'])
            time.sleep(3600)
        except requests.exceptions.RequestException:
            print(u'网络连接失败！')
            time.sleep(5)

if __name__ == '__main__':
    main()

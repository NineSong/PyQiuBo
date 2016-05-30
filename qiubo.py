#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import sys
from qiubo_student import QiuBoStudent

def main():
    if len(sys.argv) != 2:
        exit()

    while 1:
        try:
            student = QiuBoStudent(sys.argv[1])
            break
        except requests.exceptions.RequestException:
            print(u'网络连接失败')
            time.sleep(3)

    while 1:
        try:
            student.wait_for_next_course()
            student.sign_in()
            time.sleep(3900)
        except requests.exceptions.RequestException:
            print(u'网络连接失败！')
            time.sleep(3)

if __name__ == '__main__':
    main()

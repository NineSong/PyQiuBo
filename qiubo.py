#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import pyquery
import time
import json
import sys

config = {}

class QiuBo(object):
    def __init__(self):
        self._id = config['id']
        self._session = requests.Session()
        self.login()

    def login(self):
        self._session.post(
            'http://218.193.151.102/index.php/Mhs/Dhu/dologin.php',
            data = {'username': self._id, 'password': self._id[-4:]}
        )

    def get_schedule(self):
        response = self._session.get('http://218.193.151.102/index.php/Mhs/Dhu/mycourse.php')
        pq = pyquery.PyQuery(response.text)
        course_list = pq('#courselist')('.item')
        course_info = pq('.listcontent')
        begin_time = {
            0: '8:15',
            2: '10:05',
            4: '13:00',
            6: '14:50',
            9: '18:00',
            11: '19:50'
        }
        self._schedule = [[], [], [], [], [], [], []]

        for (i, div) in enumerate(course_list):
            style = pq(div).attr('style').split(';')
            name = pq(div)('a').html()
            onclick = pq(course_info[i])('a').attr('onclick').split(',')
            self._schedule[int(style[0][5:-1]) // 20].append({
                'course_name': name[:name.index('@')],
                'lesson_id': onclick[0][onclick[0].index('(') + 1:],
                'course_id': onclick[1],
                'begin_time': begin_time[int(style[1][5:-3]) // 5],
                'span_time': int(style[2][8:-3]) // 5
            });

        # print(self._schedule)

    def sign_in(self, course=None):
        if self._course is None:
            return

        if course is None:
            course = self._course

        response = self._session.get(
            'http://218.193.151.102/index.php/Mhs/Keshang/signin/lesson_id/' +
            course['lesson_id'] + '/course_id/' + course['course_id'] + '/stu_id/' + self._id
        )

        if response.json()['code'] == 1:
            print(course['course_name'] + u'签到成功！')
        else:
            print(course['course_name'] + u'签到失败！' + response.json()['reasons'])

        if 'sign_in_log' in config and config['sign_in_log']:
            if sys.version_info < (3, 0):
                course_name = course['course_name'].encode('UTF-8')
                response_text = response.text.encode('UTF-8')
            else:
                course_name = course['course_name']
                response_text = response.text

            with open('qiubo.log', 'a') as log:
                log.write(
                    time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()) +
                    ' ' + course_name + ' ' + response_text + '\n'
                )

    def wait_for_next_course(self):
        _time = time.localtime()
        _day = _time.tm_wday
        _hour = _time.tm_hour
        _min = _time.tm_min
        schedule_today = self._schedule[_day]

        for course in schedule_today:
            begin_time = course['begin_time'].split(':')
            minutes = (int(begin_time[0]) - _hour)*60 + int(begin_time[1]) - _min

            if minutes > -45:
                self._course = course
                if minutes > 0:
                    print(course['course_name'] + u'将在%d小时%d分钟后开始' % (minutes // 60, minutes % 60))
                    time.sleep(minutes * 60)
                return

        self._course = None

def main():
    global config

    try:
        _input = raw_input
    except:
        _input = input

    try:
        with open('qiubo.json', 'r') as config_file:
            config = json.load(config_file)
    except:
        pass

    if 'id' not in config:
        config['id'] = _input("Please enter your ID: ")

    try:
        qiubo = QiuBo()
        qiubo.get_schedule()
        # qiubo.sign_in({
        #     'course_name': u'计算机专业前沿技术',
        #     'lesson_id': '11040',
        #     'course_id': '203423'
        # })
    except requests.exceptions.RequestException:
        print(u'网络连接失败！')
        exit()

    while True:
        try:
            qiubo.login()
            qiubo.wait_for_next_course()
            qiubo.sign_in()
            time.sleep(3600)
        except requests.exceptions.RequestException:
            print(u'网络连接失败！')
            time.sleep(5)

if __name__ == '__main__':
    main()

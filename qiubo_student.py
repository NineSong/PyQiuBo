# -*- coding: utf-8 -*-

import requests
import pyquery
import time
import sys
from qiubo_classair import QiuBoClassAir

class QiuBoStudent(object):
    def __init__(self, student_id, fetch_schedule=True):
        self._id = student_id
        self._name = QiuBoClassAir(self._id).name
        self._course = None
        self._schedule = None
        self._session = requests.Session()
        self._login()

        if fetch_schedule:
            self._fetch_schedule()

    def _login(self):
        self._session.post(
            'http://classair.dhu.edu.cn/index.php/Mhs/Dhu/dologin.php',
            data={'username': self._id, 'password': self._id[-4:]}
        )

    def _fetch_schedule(self):
        response = self._session.get('http://classair.dhu.edu.cn/index.php/Mhs/Dhu/mycourse.php')
        pq = pyquery.PyQuery(response.text)
        course_list = enumerate(pq('#courselist')('.item'))
        course_info = pq('.listcontent')
        begin_time = {
            0: '8:15',
            1: '9:00',
            2: '10:05',
            4: '13:00',
            6: '14:50',
            9: '18:00',
            11: '19:50'
        }
        self._schedule = [], [], [], [], [], [], []

        for i, div in course_list:
            style = pq(div).attr('style').split(';')
            name = pq(div)('a').html()
            onclick = pq(course_info[i])('a').attr('onclick').split(',')
            self._schedule[int(style[0][5:-1]) // 20].append({
                'course_name': name[:name.index('@')],
                'lesson_id': onclick[0][onclick[0].index('(') + 1:],
                'course_id': onclick[1],
                'begin_time': begin_time[int(style[1][5:-3]) // 5]
            });

    def print_schedule(self):
        if self._schedule is None:
            return

        day = u'星期一', u'星期二', u'星期三', u'星期四', u'星期五', u'星期六', u'星期日'

        for i, schedule in enumerate(self._schedule):
            if schedule:
                print(day[i])
                for course in schedule:
                    j = (course[x] for x in ('begin_time', 'course_name', 'lesson_id', 'course_id'))
                    print(' '.join(j))

    def sign_in(self, course=None, attempts=5, interval=30, log=True):
        if course is None:
            if self._course is None:
                return
            else:
                course = self._course

        succeed = False
        self._login()

        for i in range(attempts):
            response = self._session.get(
                'http://classair.dhu.edu.cn/index.php/Mhs/Keshang/signin/lesson_id/' +
                course['lesson_id'] + '/course_id/' + course['course_id'] + '/stu_id/' +
                self._id + '/lat/31.0560/lon/121.2140'
            )

            if response.json()['code'] == 1:
                items = (
                    time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()),
                    self._id, self._name, course['course_name'] + u'签到成功'
                )
                succeed = True
            else:
                items = (
                    time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()),
                    self._id, self._name, course['course_name'] + u'签到失败',
                    response.json()['reasons']
                )

            print(' '.join(items))

            if log:
                if sys.version_info < (3, 0):
                    course_name = course['course_name'].encode('UTF-8')
                    name = self._name.encode('UTF-8')
                    response_text = response.text.encode('UTF-8')
                else:
                    course_name = course['course_name']
                    name = self._name
                    response_text = response.text

                items = (
                    time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()),
                    self._id, name, course_name, response_text
                )

                with open('qiubo.log', 'a') as _log:
                    _log.write(' '.join(items) + '\n')

            if succeed:
                return
            elif i != attempts - 1:
                time.sleep(interval)

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
                    print(course['begin_time'] + ' ' + course['course_name'])
                    time.sleep(minutes * 60)
                return

        self._course = None

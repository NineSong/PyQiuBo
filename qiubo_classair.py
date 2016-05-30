# -*- coding: utf-8 -*-

import requests
# import json

class QiuBoClassAir(object):
    def __init__(self, student_id, fetch_teacher_id=False):
        self._session = requests.Session()
        response = self._session.get(
            'http://classair.dhu.edu.cn/mhs.php/Mhs/Login/doLogin',
            params={'username': student_id, 'password': student_id[-4:]}
        ).json()

        if 'results' in response:
            self.name = response['results']['stu_name']
            self._access_token = response['results']['access_token']
        else:
            self.name = u'某某某'

        if fetch_teacher_id:
            self._fetch_schedule()

    def _fetch_schedule(self):
        self._schedule = [], [], [], [], [], [], []

        course_list = requests.get(
            'http://classair.dhu.edu.cn/mhs.php/Mhs/Outline/index',
            params={'access_token': self._access_token}
        ).json()['results']['courseList']

        for course in course_list:
            # print(json.dumps(course, indent=2))
            self._schedule[course['day'] - 1].append({
                x: course[x] for x in ('course_name', 'begin_time', 'teacher_id')
            })

    def get_teacher_id(self, day, begin_time):
        for course in self._schedule[day]:
            if begin_time == course['begin_time']:
                return course['teacher_id']

        return None

    def print_teacher_id(self):
        for schedule in self._schedule:
            for course in schedule:
                print(course['course_name'] + ' ' + course['teacher_id'])

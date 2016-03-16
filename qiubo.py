#!/usr/bin/env python

import requests
import time
import sys

class SignInRobot(object):

    def __init__(self):
        self._id = sys.argv[1]
        self._session = requests.Session()
        self._access_token = self._get_token()

        if self._access_token is None:
            print('Error: failed to log in!')
            exit()

    def _get_token(self):
        response_json = self._session.get(
            'http://classair.dhu.edu.cn/mhs.php/Mhs/Login/doLogin',
            params={
                'role': 1,
                'siteid': 1,
                'university_id': 2008,
                'username': self._id,
                'password': self._id[-4:]
            }
        ).json()

        if 'results' in response_json:
            return response_json['results']['access_token']
        else:
            return None

    def get_class_schedule(self):
        schedule = []
        _dict = {
            'day': '',
            'course_id': '',
            'lesson_id': '',
            'begin_time': '',
        }

        course_list = requests.get(
            'http://classair.dhu.edu.cn/mhs.php/Mhs/Outline/index',
            params={'access_token': self._access_token}
        ).json()['results']['courseList']

        for element in course_list:
            for _key in _dict:
                _dict[_key] = element[_key]
            schedule.append(_dict.copy())
        return schedule

    def sign_in(self, course):
        response = self._session.get(
            'http://classair.dhu.edu.cn/mhs.php/Mhs/Online/signin/',
            params={
                'course_id': course['course_id'],
                'lesson_id': course['lesson_id'],
                'stu_id': self._id
            }
        )

        with open('log', 'a') as log:
            _localtime = time.localtime(time.time())
            log.write(
                'month:' + str(_localtime.tm_mon) +
                'day:' + str(_localtime.tm_mday) +
                'hour:' + str(_localtime.tm_hour) +
                'minute:' + str(_localtime.tm_min) +
                'courseId:' + course['course_id'] +
                response.text.encode('utf-8') + '\n'
            )
        time.sleep(5400)

class Timer(object):

    def __init__(self, class_schedule):
        self._list = class_schedule
        self._localtime = time.localtime(time.time())
        self._day = self._localtime.tm_wday + 1
        self._hour = self._localtime.tm_hour
        self._min = self._localtime.tm_min

    def find_course(self):
        _D_value = 0
        element = {}
        for element in self._list:
            _D_value = (element['day']-self._day) * 24 * 3600
            if _D_value >= 0:
                _D_value += self._calculate_time(element['begin_time'])
                if _D_value >= -5400:
                    break
                else:
                    continue
            else:
                continue
        element['d_value'] = _D_value
        self._sleep(element)
        return element

    def _calculate_time(self, begin_time):
        begin_time = begin_time.encode('utf-8')
        _D_hour = int(begin_time[:begin_time.index(':')]) - self._hour
        _D_min = int(begin_time[begin_time.index(':')+1:]) - self._min
        return (_D_hour*3600 + _D_min*60)

    def _sleep(self, _dict):
        _seconds = _dict['d_value']
        if _seconds > 0:
            print("Next course will start in %d minutes." % (_seconds / 60))
            time.sleep(_seconds)

def main():
    if len(sys.argv) != 2:
        print('Usage: qiubo.py ID')
        exit()

    while True:
        try:
            robot = SignInRobot()
            schedule = robot.get_class_schedule()
            timer = Timer(schedule)
            robot.sign_in(timer.find_course())
        except requests.exceptions.RequestException:
            print('Connection failed!')
            time.sleep(5)

if __name__ == '__main__':
    main()

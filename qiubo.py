#!/usr/bin/env python

import requests
import time
import sys
# import json

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
                # 'role': 1,
                # 'siteid': 1,
                # 'university_id': 2008,
                'username': self._id,
                'password': self._id[-4:]
            }
        ).json()

        if 'results' in response_json:
            return response_json['results']['access_token']
        else:
            return None

    def get_schedule(self):
        schedule = []
        _course = {
            'day': '',
            'course_name': '',
            'course_id': '',
            'lesson_id': '',
            'begin_time': '',
            'span_time': ''
        }

        course_list = requests.get(
            'http://classair.dhu.edu.cn/mhs.php/Mhs/Outline/index',
            params={'access_token': self._access_token}
        ).json()['results']['courseList']

        for course in course_list:
            # print(json.dumps(course, indent=2))
            for key in _course:
                _course[key] = course[key]
            schedule.append(_course.copy())
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

        with open('qiubo.log', 'a') as log:
            log.write(
                time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()) + ' ' +
                course['course_name'].encode('utf-8') + ' ' +
                response.text.encode('utf-8') + '\n'
            )

        if response.json()['code'] == 1:
            print(course['course_name'] + ' sign in succeeded!')
            time.sleep(5400)
        else:
            print(course['course_name'] + ' sign in failed!')


class Timer(object):

    def __init__(self, schedule):
        self._schedule = schedule
        localtime = time.localtime(time.time())
        self._day = localtime.tm_wday + 1
        self._hour = localtime.tm_hour
        self._min = localtime.tm_min

    def find_course(self):
        for course in self._schedule:
            if course['day'] < self._day:
                continue
            countdown = (course['day']-self._day) * 24 * 60 + self._countdown(course['begin_time'])
            if countdown >= -45:
                break

        course['countdown'] = countdown
        self._sleep(course)
        return course

    def _countdown(self, begin_time):
        begin_time = begin_time.encode('utf-8')
        hours = int(begin_time[:begin_time.index(':')]) - self._hour
        minutes = int(begin_time[begin_time.index(':')+1:]) - self._min
        return (hours*60 + minutes)

    def _sleep(self, course):
        minutes = course['countdown']
        if minutes > 0:
            h = minutes / 60
            m = minutes % 60
            print(course['course_name'] + ' will start in %dh %dm.' % (h, m))
            print('Waiting for the course to start.')
            time.sleep(minutes * 60)

def main():
    if len(sys.argv) != 2:
        print('Usage: qiubo.py ID')
        exit()

    while True:
        try:
            robot = SignInRobot()
            schedule = robot.get_schedule()
            timer = Timer(schedule)
            robot.sign_in(timer.find_course())
        except requests.exceptions.RequestException:
            print('Connection failed!')
            time.sleep(5)
        except KeyboardInterrupt:
            print('\b\bExiting :)')
            exit()

if __name__ == '__main__':
    main()

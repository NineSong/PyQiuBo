#!/usr/bin/env python

import requests
import time

class SearchAllLessonId(object):
    """docstring for SearchAllLessonId"""
    def __init__(self):
        self.id = raw_input("Please enter your ID: ")
        self.access_token = ''
        # self.url = 'http://classair.dhu.edu.cn/mhs.php/Mhs/'
        self.session = requests.Session()

    def Get_token(self):
        password = self.id[-4:]
        first_url = 'http://classair.dhu.edu.cn/mhs.php/Mhs/Login/doLogin?password=' + password + '&role=1&siteid=1&university_id=2008&username=' + self.id
        first_page = self.session.get(first_url)
        self.access_token = first_page.json()['results']['access_token']

    def Get_course_list(self):
        _list = []
        _dict = {
            'day': '',
            'course_id': '',
            'lesson_id': '',
            'begin_time': '',
        }
        self.Get_token()
        Index_Url = 'http://classair.dhu.edu.cn/mhs.php/Mhs/Outline/index?access_token=' + self.access_token
        re_index = requests.get(Index_Url)
        for element in re_index.json()['results']['courseList']:
            for _key in _dict:
                _dict[_key] = element[_key]
            _list.append(_dict.copy())
        return _list

    def sign_in(self, _dict):
        _sign_url = 'http://classair.dhu.edu.cn/mhs.php/Mhs/Online/signin/?'
        _sign_url += 'course_id=' + _dict['course_id']
        _sign_url += '&lesson_id=' + _dict['lesson_id']
        _sign_url += '&stu_id=' + id
        _text = self.session.get(_sign_url)
        with open('log','a') as log:
            _localtime = time.localtime(time.time())
            log.write('month:' + str(_localtime.tm_mon))
            log.write('day:' + str(_localtime.tm_mday))
            log.write('hour:' + str(_localtime.tm_hour))
            log.write('minute:' + str(_localtime.tm_min))
            log.write('courseId:' + _dict['course_id'])
            log.write(_text.text.encode('utf-8'))
            log.write('\n')
        time.sleep(5400)

class TimeControl(object):
    """docstring for TimeControl"""
    def __init__(self, _list):
        self._list = _list
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
                _D_value += self.calculate_time(element['begin_time'])
                if _D_value >= -5400:
                    break
                else:
                    continue
            else:
                continue
        element['d_value'] = _D_value
        self._sleep(element)
        return element

    def calculate_time(self, begin_time):
        begin_time = begin_time.encode('utf-8')
        _D_hour = int(begin_time[:begin_time.index(':')]) - self._hour
        _D_min = int(begin_time[begin_time.index(':')+1:]) - self._min
        return (_D_hour*3600 + _D_min*60)

    def _sleep(self,_dict):
        _seconds = _dict['d_value']
        if _seconds > 0:
            print("Next course will start in %d minutes." % (_seconds / 60))
            time.sleep(_seconds)

def main():
    while True:
        S = SearchAllLessonId()
        _list = S.Get_course_list()
        T = TimeControl(_list)
        S.sign_in(T.find_course())

if __name__ == '__main__':
    main()

#!/usr/bin/env python
import requests
import time
SchoolNumber = '141320131'
class SearchAllLessonId(object):
    """docstring for SearchAllLessonId"""
    def __init__(self):
        self.acc_token = ''
        self.url_text = ''
        self.cookies = ''
        self.url = 'http://classair.dhu.edu.cn/mhs.php/Mhs/'
        self.S = requests.Session()
    def Get_totken(self):
        Password = SchoolNumber[-4:]
        First_Url = self.url + 'Login/doLogin' + '?password='+Password+'&role=1&siteid=1&university_id''=2008'+'&username='+ SchoolNumber
        first_page = self.S.get(First_Url)
        self.cookies = first_page.headers['Set-Cookie'].split(';')[0]
        #What you get is unicode type and you need convert it to string
        #And use some funstion to process
        #print(re_one.text)
        first_page_encode = first_page.text.encode('utf-8')
        #first_page_encode is the string type of the text
        first_page_encode = first_page_encode[first_page_encode.find('access_token')+len('access_token'):]
        for character in first_page_encode:
            if character.isalnum():
                self.acc_token += character
            if character == ',':
                break

    def Get_course_list(self):
        _list = []
        _dict = {
        'day':'',
        'course_id':'',
        'lesson_id':'',
        'begin_time':'',
        }
        self.Get_totken()
        Index_Url = 'http://classair.dhu.edu.cn/mhs.php/Mhs/Outline/index?access_token=' + self.acc_token
        re_index = requests.get(Index_Url)
        for element in re_index.json()['results']['courseList']:
            for _key in _dict:
                _dict[_key] = element[_key]
            _list.append(_dict.copy())
        return _list

    def sign_in(self,_dict):
        _sign_url = 'http://classair.dhu.edu.cn/mhs.php/Mhs/Online/signin/?'
        _sign_url += 'course_id=' + _dict['course_id']
        _sign_url += '&lesson_id=' + _dict['lesson_id']
        _sign_url += '&stu_id=' + SchoolNumber
        _text = self.S.get(_sign_url)
        with open('log','a') as log:
            _localtime = time.localtime(time.time())
            log.write('month:' + str(_localtime.tm_mon))
            log.write('day:' + str(_localtime.tm_mday))
            log.write('hour:' +str(_localtime.tm_hour))
            log.write('minute:' + str(_localtime.tm_min))
            log.write('courseId:' + _dict['course_id'])
            log.write(_text.text.encode('utf-8'))
            log.write('\n')
        time.sleep(5400)

class Time_Control(object):
    """docstring for Time_Control"""
    def __init__(self, _list):
        self._list = _list
        self._localtime = time.localtime(time.time())
        self._day = self._localtime.tm_wday + 1
        #because the localtime return the week day from 0 to 6
        self._hour = self._localtime.tm_hour
        self._min = self._localtime.tm_min
    def find_course(self):
        _D_value = 0
        element = {}
        for element in self._list:
            _D_value = (element['day'] - self._day)*24*3600
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

    def calculate_time(self,begin_time):
        begin_time = begin_time.encode('utf-8')
        _D_hour = int(begin_time[:begin_time.index(':')]) - self._hour
        _D_min = int(begin_time[begin_time.index(':')+1:]) - self._min
        return (_D_hour*3600 + _D_min*60)


    def _sleep(self,_dict):
        _seconds = _dict['d_value']
        if _seconds > 0:
            print("Now we need to sleep %d seconds" % _seconds)
            time.sleep(_seconds)

def main():
    while True:
        S = SearchAllLessonId()
        _list = S.Get_course_list()
        T = Time_Control(_list)
        S.sign_in(T.find_course())

if __name__ == '__main__':
    main()

import requests
import pyquery

class QiuBoTeacher(object):
    def __init__(self, teacher_id):
        self._session = requests.Session()
        self._session.post(
            'http://classair.dhu.edu.cn/teacherd.php/dht/login/dologin.php',
            data={'username': teacher_id, 'password': teacher_id[-4:]}
        )

    def students_signin(self):
        response = self._session.get(
            'http://classair.dhu.edu.cn/teacherd.php/dht/online/index/tpl/studentsignin.php'
        )
        pq = pyquery.PyQuery(response.text)

        if pq('.ask') is None:
            return

        student = []

        for stu in pq('.ask'):
            student.append(pq(stu).attr('href')[:-4].split('/')[6])

        return student

    def students_unsignin(self):
        response = self._session.get(
            'http://classair.dhu.edu.cn/teacherd.php/dht/online/index/tpl/studentunsignin.php'
        )
        pq = pyquery.PyQuery(response.text)

        if pq('.ask') is None:
            return

        student = []

        for stu in pq('.ask'):
            student.append(pq(stu).attr('href')[:-4].split('/')[6])

        return student

# PyQiuBo
A Python script that helps students sign in DHU QiuBo app.

# Prerequisite
- [Python 2.7/3.4](https://www.python.org/downloads/)
- [requests](https://pypi.python.org/pypi/requests)
- [pyquery](https://pypi.python.org/pypi/pyquery)

Note: Other versions of Python 2/3 may work but are untested.

# Usage
Run `qiubo.py your_student_id`. Have fun!

# Tips
- The script relies on the clock of your computer, so make sure that your clock is correct.
- PE lessons do not appear in Yiban's schedule.
- If two or more courses conflict, only one of them can be signed in.
- Sometimes sign-in may fail. Don't worry, this may be because their database is corrupted.

# Log
`qiubo.log` consists of the time it tried to sign in, student id, student name, course name and the JSON returned by the server.
`"code": 1` stands for success while `"code": -1` stands for failure.

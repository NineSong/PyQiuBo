# QiuBo
A Python script that helps students sign in DHU QiuBo app.

# Prerequisite
- [Python 2.7/3.4](https://www.python.org/downloads/)
- [requests](https://pypi.python.org/pypi/requests)
- [pyquery](https://pypi.python.org/pypi/pyquery)

Note: Other versions of Python 2/3 may work but are untested.

# Usage
First, edit the configuration file `qiubo.json`.
Fill in your student id which is mandatory for obvious reasons.

`sign_in_log` controls whether to produce a sign-in log on each sign-in attempt.
The log will be named `qiubo.log`.

Then, run `qiubo.py`. Have fun!

# Reminders
- The script relies on the clock of your computer, so make sure that your clock is correct.
- PE lessons do not appear in Yiban's schedule.
- Sometimes sign-in may fail. Don't worry, check out the course first.
  It doesn't matter if it is not a major course.

# Log
`qiubo.log` simply consists of the time it tried to sign in and the JSON returned by the server.
`"code": 1` stands for success while `"code": -1` stands for failure.

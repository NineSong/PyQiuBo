# QiuBo
A Python script that helps students sign in DHU QiuBo app.

# Prerequisite
- [Python 2.7/3.4](https://www.python.org/downloads/)
- [requests](https://pypi.python.org/pypi/requests)
- [pyquery](https://pypi.python.org/pypi/pyquery)

Note: Other versions of Python 2/3 may work but are untested.

# Usage
First, edit the configuration file `qiubo.json`.
Fill in your studend id which is mandatory for obvious reasons.

The `sign_in_log` item controls whether to produce a sign-in log on each sign-in attempt.
The log will be named `qiubo.log`.

More configurable items are coming.

# Log
`qiubo.log` simply consists of the time it tried to sign in and the JSON returned by the server.
`"code": 1` stands for success while `"code": -1` stands for failure.

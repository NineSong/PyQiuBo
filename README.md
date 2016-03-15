# QiuBo
A Python script that helps students sign in DHU QiuBo app.

# Prerequisite
- [Python 2.x](https://www.python.org/downloads/)
- [requests](https://pypi.python.org/pypi/requests)

`requests` can be installed through [`pip`](https://pypi.python.org/pypi/pip).
With `pip` installed, execute `pip install requests` in a shell.

# Usage
Pass your student ID as a command-line parameter.

e.g. If your student ID is 1234567890, execute in a shell
```
user ~ $ /path/to/QiuBo/qiubo.py 1234567890
```

# Log
The script generates log file in its directory if there is any sign-in attempt.
It simply consists of the time it tries to sign in and the JSON returned by the server.
If the JSON contains `code: 1`, it means that the attempt was successful.

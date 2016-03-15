# QiuBo
A Python script that helps students sign in DHU QiuBo app.

# Prerequisite
- [Python 2.x](https://www.python.org/downloads/)
- [requests](https://pypi.python.org/pypi/requests)

`requests` can be installed through [`pip`](https://pypi.python.org/pypi/pip).
With `pip` installed, execute `pip install requests` in a shell.

# Log
The script generates log file in its directory if there is any sign-in attempt.
It simply consists of the time it tries to sign in and the JSON returned by the server.
If the JSON contains `code:1`, it means that the attempt was successful.

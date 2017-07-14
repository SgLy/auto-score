## Auto Score

Education system moved to NetID this semester. While NetID login require no CAPTCHA, we are available to work again :)

Aims to automatically fetch grade and notify by sending email.

Designed for SYSU.

Tested under Windows 7. (Linux should also work)


### Usage:
1. create `mail_account.py` under `config` folder, containing your account to send and receive email;

> `virtualenv` is recommended

2. `virtualenv -p /usr/bin/python3 env`;
3. `env/bin/pip install -r requirements.txt`;
4. `./main.py`.

> without `virtualenv`

2. `pip install -r requirements.txt`;
3. `python3 main.py`.

### Example:
```python
# filename: mail_account.py

sender = 'me@mail.163.com'
passwd = 'myMAILaccountPASSWORD'
smtp_server = 'smtp.163.com'
```

### Test
Codes are produced under `Windows 7 Ultimate, Service Pack 1`, with `Python 3.5.1`.

If it worked successfully under other environment, please let me know and I'll add it here; if it break, please leave me an issue.

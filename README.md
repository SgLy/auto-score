## Auto Score

Education system moved to NetID this semester. While NetID login require no CAPTCHA, we are available to work again :)

Aims to automatically fetch grade and notify by sending email.

Designed for SYSU.


### Usage:
1. create `mail_account.py` under `config` folder, containing your account to send email;
1. use `pip` to install requirements (`pip install -r requirements.txt`)
1. run `auto_score.py` (`python3 auto_score.py`)

#### Use in your own code
```python
from auto_score import auto_score
info = {
    'netid': 'your_netid',
    'passwd': 'your_password',
    'mail': 'email@receiving.notification'
}
a = auto_score(info)
a.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('Interrupted')
```
_Every `auto_score` instance contains a deamonized thread to query grade. To keep querying, do some looping like above._

#### `config/mail_account.py`:
```python
# filename: config/mail_account.py

sender = 'me@mail.163.com'
passwd = 'myMAILaccountPASSWORD'
smtp_server = 'smtp.163.com'
```

### Test
Codes are produced under `Windows 7 Ultimate, Service Pack 1`, with `Python 3.5.1`.

Tested under:
1. `Ubuntu 17.04` with `Python 3.5.3`

If it worked successfully under other environment, please let me know and I'll add it here; if it break, please leave me an issue.
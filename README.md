## Auto Score

This is a __Selenium__ fork, which requires a __GUI browser__. Captcha must be manually input.

Aims to automatically fetch grade and notify by sending email.

Designed for SYSU.

Currently only for linux.


### Requires:
- [`Google Chromium`](https://www.chromium.org/Home) or other browser that supports [`SeleniumHQ`](http://www.seleniumhq.org/)

> if you use a browser besides chromium, please change `auto_score.py:6` to corresponding browser, such as `driver = webdriver.FireFox()`. For all supported browsers, please read document of Selenium.

### Usage:
1. create `mail_account.py` under `config` folder, containing your account to send and receive email;
2. compile result-generating module, like `g++ generate.cpp -o generate`;

> `virtualenv` is recommended

3. `virtualenv -p /usr/bin/python3 env`;
4. `env/bin/pip install -r requirements.txt`;
5. `./main.py`.

> without `virtualenv`

3. `pip install -r requirements.txt`;
4. `python3 main.py`.

### Example:
```python
# filename: mail_account.py

source = 'me@mail.163.com'
destination = 'mail@to.receive.notification'
passwd = 'myMAILaccountPASSWORD'
smtp_server = 'smtp.163.com'
```

### Test
Codes are produced under up-to-date `ArchLinux`, with `Python 3.6` and `g++ (GCC) 6.3.1`.

If it worked successfully under other environment, please let me know and I'll add it here; if it break, please leave me an issue.

## Auto Score

### Due to Geetest captcha, this system is not working now.

Aims to automatically fetch grade and notify by sending email.
Designed for SYSU.

Currently only for linux.


### Requires:
1. `tesseract`

### Usage:
1. create `mail_account.py` under `config` folder, containing your account to send email;
2. create `id_list.py` under `config` folder, containing your id to fetch grade;
3. compile result-generating module, like `g++ generate.cpp -o generate`;
4. `./main.py` or `python3 main.py`.

### Example:
```python
# filename: mail_account.py

me = 'me@mail.163.com'
passwd = 'myMAILaccountPASSWORD'
smtp_server = 'smtp.163.com'
```

```python
# filename: id_list.py

id_list   = [15300100, 16100123]
pass_list = ['01011234', '1231789X']
mail_list = ['mail@to.receive', 'notification@when.grade.changed']
```

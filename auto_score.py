import requests
import re, json
from bs4 import BeautifulSoup

def login(netid, passwd):
    s = requests.session()
    url = 'https://cas.sysu.edu.cn/cas/login?service=http://uems.sysu.edu.cn/jwxt/casLogin?_tocasurl=http://wjw.sysu.edu.cn/cas'
    soup = BeautifulSoup(s.get(url).content, 'lxml')
    data = {
        'username': netid,
        'password': passwd,
        'lt': soup.select('[name=lt]')[0]['value'],
        'execution': soup.select('[name=execution]')[0]['value'],
        '_eventId': 'submit',
        'submit': 'LOGIN'
    }
    r = s.post(url, data = data)
    if r.status_code != requests.codes.ok:
        raise RuntimeError('Network error! Status code: %d' % r.status_code)
    if r.content.decode('utf-8', 'ignore').find('Invalid credentials.') != -1:
        raise RuntimeError('Invalid credentials.')
    url = re.findall(r'(http.+?)"', r.content.decode('utf-8'))[0]
    r = s.get(url)
    if r.status_code != requests.codes.ok:
        raise RuntimeError('Network error! Status code: %d' % r.status_code)
    return s

def getScore(s):
    r = s.get('http://wjw.sysu.edu.cn/api/score')
    
    res = r.content
    res = re.findall(data_re, r.content.decode('utf-8'))[0].replace('\\/', '/')
    return json.loads(res)

def toFile(grade, add):
    with open('config/category.txt', 'r') as f:
        keys = f.read().split('\n')[:-1]
    with open(add, 'w') as f:
        f.write('%d\n' % len(grade))
        for g in grade:
            for k in keys:
                try:
                    s = g[k]
                except KeyError:
                    s = ''
                f.write('%s\n' % s)

data_re = re.compile(r'primary:(\[.+?\])')

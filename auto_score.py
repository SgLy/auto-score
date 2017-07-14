import requests
import re, json
from bs4 import BeautifulSoup
from util import *

class auto_score:
    def __init__(self, info):
        self.info = info
        self.session = None

    def getScore(self):
        if self.session is None:
            writeLog('No session existing. First time login')
            self.session = self.__tryLogin__()

        while True:
            r = self.session.get('http://wjw.sysu.edu.cn/api/score')
            if r.content.decode('utf-8').find('expired') == -1:
                break
            # Session expired
            print('Session expired. Retry login...')
            self.session = self.__tryLogin__()

        res = r.content.decode('utf-8')
        res = re.findall(r'primary:(\[.+?\])', res)[0].replace('\\/', '/')
        return json.loads(res)

    def __tryLogin__(self):
        writeLog('Try logging in %s' % self.info['netid'])
        try:
            s = self.__login__()
        except RuntimeError as err:
            print(err)
            quit()
        else:
            print('Successfully logged in.')
            return s

    def __login__(self):
        s = requests.session()
        url = 'https://cas.sysu.edu.cn/cas/login?service=http://uems.sysu.edu.cn/jwxt/casLogin?_tocasurl=http://wjw.sysu.edu.cn/cas'
        soup = BeautifulSoup(s.get(url).content, 'lxml')
        data = {
            'username': self.info['netid'],
            'password': self.info['passwd'],
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
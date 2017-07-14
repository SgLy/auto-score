#!env/bin/python
from util import *
from fetcher import fetcher
import compare

import threading
import os, time, json, getpass
from random import randint

class auto_score:
    def __init__(self, info, language = 'CHN'):
        self.info = info
        self.language = language
        self.WAIT_TIME = 300
        self.WAIT_TIME_RANDOM_RANGE = 100
        self.fetcher = fetcher(self.info)

        self.filename = os.path.join('userdata', self.info['netid'] + '.json')
        if not os.path.isfile(self.filename):
            with open(self.filename, 'w') as f:
                json.dump([], f)

    def start(self):
        threading.Thread(target = self.__run__).start()

    def __run__(self):
        while True:
            writeLog(self.info['netid'], 'Query grade')
            new_grade = self.fetcher.getScore()
            with open(self.filename, 'r') as f:
                old_grade = json.load(f)

            if new_grade == old_grade:
                writeLog(self.info['netid'], 'No updates detected.')
            else:
                writeLog(self.info['netid'], 'Updates detected, compare old and new grades')
                content = compare.compareGrade(old_grade, new_grade, self.language)

                writeLog(self.info['netid'], 'Send mail to %s' % self.info['mail'])
                title = '成绩有变动' if self.language == 'CHN' else 'Grade updated'
                sendMail(title, content, self.info['mail'], isHtml = False)

                writeLog(self.info['netid'], 'Override old grade')
                with open(self.filename, 'w') as f:
                    json.dump(new_grade, f)

            t = self.WAIT_TIME + randint(-self.WAIT_TIME_RANDOM_RANGE, self.WAIT_TIME_RANDOM_RANGE)
            writeLog(self.info['netid'], 'Wait %d seconds for next query' % t)
            time.sleep(t)

if not os.path.exists('userdata'):
    os.mkdir('userdata')

if __name__ == '__main__':
    a = []
    while True:
        print('Account #%d:' % len(a))
        a.append(auto_score({
            'netid': input('NetID: '),
            'passwd': getpass.getpass(),
            'mail': input('Email: ')
        }))
        if not input('Input one more account? (Yy)') in ['y', 'Y']:
            break
    for i in a:
        i.start()

#!env/bin/python
from util import *
import auto_score, compare, mail
import os, time, json
from random import randint

# CHN ENG
LANG = 'ENG'
WAIT_TIME = 300
WAIT_TIME_RANDOM_RANGE = 100

from config.info import info
if not os.path.exists('userdata'):
    os.mkdir('userdata')
filename = os.path.join('userdata', info['netid'] + '.json')

if not os.path.isfile(filename):
    with open(filename, 'w') as f:
        json.dump([], f)

AS = auto_score.auto_score(info)
while True:
    writeLog('Query grade')
    new_grade = AS.getScore()
    with open(filename, 'r') as f:
        old_grade = json.load(f)

    if new_grade != old_grade:
        writeLog('Updates detected.')
        content = compare.compareGrade(old_grade, new_grade, language = LANG)
        writeLog('Send mail to %s' % info['mail'])
        title = '成绩有变动' if LANG == 'CHN' else 'Grade updated'
        mail.sendMail(title, content, info['mail'], isHtml = False)
        writeLog('Override old grade')
        with open(filename, 'w') as f:
            json.dump(new_grade, f)
    else:
        writeLog('No updates detected.')

    t = WAIT_TIME + randint(-WAIT_TIME_RANDOM_RANGE, WAIT_TIME_RANDOM_RANGE)
    writeLog('Wait %d seconds for next query' % t)
    time.sleep(t)

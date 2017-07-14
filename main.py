#!env/bin/python
from util import *
import auto_score, compare
import os, time, json
from random import randint

# CHN ENG
LANG = 'CHN'
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
    writeLog(info['netid'], 'Query grade')
    new_grade = AS.getScore()
    with open(filename, 'r') as f:
        old_grade = json.load(f)

    if new_grade == old_grade:
        writeLog(info['netid'], 'No updates detected.')
    else:
        writeLog(info['netid'], 'Updates detected, compare old and new grades')
        content = compare.compareGrade(old_grade, new_grade, language = LANG)

        writeLog(info['netid'], 'Send mail to %s' % info['mail'])
        title = '成绩有变动' if LANG == 'CHN' else 'Grade updated'
        sendMail(title, content, info['mail'], isHtml = False)

        writeLog(info['netid'], 'Override old grade')
        with open(filename, 'w') as f:
            json.dump(new_grade, f)

    t = WAIT_TIME + randint(-WAIT_TIME_RANDOM_RANGE, WAIT_TIME_RANDOM_RANGE)
    writeLog(info['netid'], 'Wait %d seconds for next query' % t)
    time.sleep(t)

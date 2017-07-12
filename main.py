#!env/bin/python
import auto_score, mail
import os, sys
import markdown
# from inlinestyler.utils import inline_css
import premailer
import datetime, time
from random import randint

# CHN ENG
LANG = 'ENG'
LOGFILE = 'auto_score.log'
WAIT_TIME = 300
WAIT_TIME_RANDOM_RANGE = 100

def writeLog(s):
    with open(LOGFILE, 'a') as f:
        f.write('[%s] ' % datetime.datetime.today().isoformat())
        f.write(s + '\n')
    print(s)

def getContent(filename):
    with open(filename, 'r') as f:
        return f.read()

def writeContent(filename, content):
    with open(filename, 'w') as f:
        f.write(content)

isWin32 = sys.platform == 'win32'
if isWin32:
    writeLog('Windows OS detected')
else:
    writeLog('Non-Windows OS detected')

from config.info import info
folder = os.path.join('userdata', info['netid'])
new_file = os.path.join(folder, 'new')
old_file = os.path.join(folder, 'old')
out_file = os.path.join(folder, 'out')

if not os.path.exists(folder):
    if isWin32:
        os.system('md %s' % folder)
    else:
        os.system('mkdir -p %s' % folder)
if not os.path.isfile(old_file):
    writeContent(old_file, '0\n')

writeLog('Logging in to %s' % info['netid'])
try:
    s = auto_score.login(info['netid'], info['passwd'])
except RuntimeError as err:
    print(err)
    quit()
else:
    print('Successfully logged in')
while True:
    writeLog('Query grade')
    grade = auto_score.getScore(s)
    auto_score.toFile(grade, new_file)

    writeLog('Compare old and new grades')
    if isWin32:
        os.system('generate.exe %s %s %s -%s -MARKDOWN >> %s' %\
            (old_file, new_file, out_file, LANG, LOGFILE))
    else:
        os.system('./generate %s %s %s -%s -MARKDOWN >> %s' %\
            (old_file, new_file, out_file, LANG, LOGFILE))
    content = getContent(out_file)

    if len(content) != 0:
        writeLog('Compile markdown')
        content = markdown.markdown(content, extensions=['markdown.extensions.tables'])
        writeLog('Inline CSS')
        content = getContent('template/head.html') + content + getContent('template/tail.html')
        content = premailer.transform(content)

        writeLog('Send mail to %s' % info['mail'])
        title = '成绩有变动' if LANG == 'CHN' else 'Grade updated'
        mail.sendMail(title, content, info['mail'], True)
    writeLog('Override old grade')
    if isWin32:
        os.system('del %s' % out_file)
        os.system('move %s %s' % (new_file, old_file))
    else:
        os.system('rm %s' % out_file)
        os.system('mv %s %s' % (new_file, old_file))

    t = WAIT_TIME + randint(-WAIT_TIME_RANDOM_RANGE, WAIT_TIME_RANDOM_RANGE)
    writeLog('Wait %d seconds for next query' % t)
    time.sleep(t)

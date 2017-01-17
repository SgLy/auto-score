#!env/bin/python
import auto_score, mail
import os
import markdown
from inlinestyler.utils import inline_css
import datetime, time
from random import randint

# CHN ENG
lang = 'CHN'
user = { 'mail': '775150558@qq.com' }
logfile = 'auto_score.log'
wait_time = 300
wait_time_random_range = 100

def writeLog(s):
    with open(logfile, 'a') as f:
        f.write('[%s] ' % datetime.datetime.today().isoformat())
        f.write(s + '\n')
    print(s)

def getContent(filename):
    with open(filename,'r') as f:
        res = f.read()
    return res

def writeContent(filename, content):
    f = open(filename, 'w')
    f.write(content)
    f.close()

folder = 'userdata'
new_file = '%s/new' % folder
old_file = '%s/old' % folder
out_file = '%s/out' % folder
if not os.path.exists(folder):
    os.system('mkdir %s' % folder)
if not os.path.isfile(old_file):
    writeContent(old_file, '0\n')

writeLog('Start browser and login')
driver = auto_score.login()
while True:
    writeLog('Query grade')
    grade = auto_score.getScore(driver)
    auto_score.toFile(grade, new_file)

    writeLog('Compare old and new grades')
    os.system('./generate %s %s %s -%s -MARKDOWN >> %s' % (old_file, new_file, out_file, lang, logfile))
    content = getContent(out_file)

    if len(content) != 0:
        writeLog('Compile markdown')
        content = markdown.markdown(content, extensions=['markdown.extensions.tables'])
        writeLog('Inline CSS')
        content = getContent('template/head.html') + content + getContent('template/tail.html')
        content = inline_css(content)

        writeLog('Send mail to %s' % user['mail'])
        title = '成绩有变动' if lang == 'CHN' else 'Grade updated'
        mail.sendMail(title, content, user['mail'], True)
    writeLog('Override old grade')
    os.system('rm %s' % out_file)
    os.system('mv %s %s' % (new_file, old_file))

    t = wait_time + randint(-wait_time_random_range, wait_time_random_range)
    writeLog('Wait %d seconds for next query' % t)
    time.sleep(t)

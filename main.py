#!env/bin/python
import auto_score
import mail
import os
import markdown
import pynliner

from config.id_list import id_list

# CHN ENG
lang = 'ENG'

def getContent(filename):
    with open(filename,'r') as f:
        res = f.read()
    return res

def writeContent(filename, content):
    f = open(filename, 'w')
    f.write(content)
    f.close()

for user in id_list:
    folder = 'userdata/%s' % user['id']
    new_file = '%s/new' % folder
    old_file = '%s/old' % folder
    out_file = '%s/out' % folder
    if not os.path.exists(folder):
        os.system('mkdir %s' % folder)
    if not os.path.isfile(old_file):
        writeContent(old_file, '0\n')
    grade = auto_score.getGrade(user['id'], user['passwd'])
    auto_score.printRaw(grade, new_file)
    os.system('./generate %s %s %s -%s -MARKDOWN' % (old_file, new_file, out_file, lang))
    content = getContent(out_file)

    if len(content) != 0:
        tra = markdown.markdown(content, extensions=['markdown.extensions.tables'])
        tra = getContent('template/head.html') + tra + getContent('template/tail.html')
        tra = pynliner.Pynliner().from_string(tra).run()
        writeContent('tmp.html', tra)

        tile = getContent('config/title_%s.txt' % lang)
        mail.sendMail(title, 'tmp.html', user['mail'], True)
        os.system('rm tmp.html')
    os.system('rm %s' % out_file)
    os.system('mv %s %s' % (new_file, old_file))

from util import *

KEY = 'resource_id'
PRINTED_KEY = ['xnd', 'xq', 'kcmc', 'jsxm', 'xf', 'zzcj', 'jd', 'jxbpm']

def calcGPA(grade):
    score = 0
    credit = 0
    for i in grade:
        score += float(i['jd']) * float(i['xf'])
        credit += float(i['xf'])
    if credit != 0:
        return score / credit
    else:
        return 0.0

def compareGrade(old_grade, new_grade, language = 'ENG'):
    writeLog('Compare old and new grades')
    # Rebuild
    new = dict([(u[KEY], u) for u in new_grade])
    old = dict([(u[KEY], u) for u in old_grade])

    # Added grade
    added = []
    for i in new:
        if not i in old:
            added.append(new[i])

    # Removed
    removed = []
    for i in old:
        if not i in new:
            removed.append(old[i])

    # Modified
    modified = []
    for i in old:
        if i in new and old[i] != new[i]:
            modified.append((old[i], new[i]))

    gpa = (calcGPA(old_grade), calcGPA(new_grade))
    return renderText(added, removed, modified, gpa, language)

PATTERN_ENG = '''You have %d grade updates, and GPA changed from %.2f to %.2f. Below listed these updates:

%s

Please wait for our new version to also include detailed informations of your score.
Proudly powered by SgLy
'''
TITLES_ENG = ['Added grade', 'Removed grade', 'Modified grade']
KEYS_ENG = {
    'xnd': 'Year',
    'xq': 'Semester',
    'kcmc': 'Course name',
    'jsxm': 'Teacher name',
    'xf': 'Credit',
    'zzcj': 'Final score',
    'jd': 'Grade point',
    'jxbpm': 'Rank'
}
PATTERN_CHN = '''你的成绩有%d处变动，平均绩点由%.2f变为%.2f。以下是所有变动：

%s

新版本将加入分数的详细信息，敬请期待！
Proudly powered by SgLy
'''
KEYS_CHN = {
    'xnd': u'学年度',
    'xq': u'学期',
    'kcmc': u'课程名称',
    'jsxm': u'教师姓名',
    'xf': u'学分',
    'zzcj': u'最终成绩',
    'jd': u'绩点',
    'jxbpm': u'教学班排名'
}
TITLES_CHN = [u'成绩新增', u'成绩删除', u'成绩变动']
def renderText(added, removed, modified, gpa, language):
    if language == 'ENG':
        pattern = PATTERN_ENG
        titles = TITLES_ENG
        keys = KEYS_ENG
    elif language == 'CHN':
        pattern = PATTERN_CHN
        titles = TITLES_CHN
        keys = KEYS_CHN
    else:
        writeLog('Language error: %s translation not found' % language)
        quit()

    detail = u''

    for i, a in enumerate(added):
        detail += '[%s #%d]\n' % (titles[0], i)
        for k in PRINTED_KEY:
            try:
                detail += '%s: %s\n' % (keys[k], a[k])
            except KeyError:
                detail += '%s:\n' % keys[k]
        detail += '\n'

    for i, r in enumerate(removed):
        detail += '[%s #%d]\n' % (titles[1], i)
        for k in PRINTED_KEY:
            try:
                detail += '%s: %s\n' % (keys[k], r[k])
            except KeyError:
                detail += '%s:\n' % keys[k]
        detail += '\n'

    for i, o, n in enumerate(modified):
        detail += '[%s #%d]\n' % (titles[2], i)
        for k in PRINTED_KEY:
            try:
                detail += '%s: %s -> %s\n' % (keys[k], o[k], n[k])
            except KeyError:
                detail += '%s:\n' % keys[k]
        detail += '\n'

    total_len = len(added) + len(removed) + len(modified)
    
    return pattern % (total_len, gpa[0], gpa[1], detail)
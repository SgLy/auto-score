import sys, datetime

LOGFILE = 'auto_score.log'
def writeLog(s):
    with open(LOGFILE, 'a') as f:
        f.write('[%s] ' % datetime.datetime.today().isoformat())
        f.write(s + '\n')
    print(s)
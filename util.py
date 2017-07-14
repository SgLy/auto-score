import sys, datetime

LOGFILE = 'auto_score.log'
def writeLog(netid, content):
    with open(LOGFILE, 'a') as f:
        time = datetime.datetime.today().isoformat()
        f.write('[%s] (%s) %s\n' % (time, netid, content))
    print('(%s) %s' % (netid, content))

# mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.mail_account import sender, passwd, smtp_server

def sendMail(title, content, destination, isHtml):
    msg = MIMEMultipart('alternative')
    msg.attach(MIMEText(content, 'html' if isHtml else 'plain'))

    msg['Subject'] = title
    msg['From'] = sender
    msg['To'] = destination

    with smtplib.SMTP(smtp_server) as smtp:
        smtp.starttls()
        smtp.login(sender, passwd)
        smtp.sendmail(sender, [destination], msg.as_string())
        smtp.quit()

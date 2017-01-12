import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.mail_account import me, passwd, smtp_server

def sendMail(title, filename, des, isHtml):
    you = des
    
    msg = MIMEMultipart('alternative')

    with open(filename, 'rb') as fb:
        if isHtml:
            msg.attach(MIMEText(fp.read(), 'html'))
        else:
            msg.attach(MIMEText(fp.read(), 'plain'))

    msg['Subject'] = title
    msg['From'] = me
    msg['To'] = you

    s = smtplib.SMTP(smtp_server)
    s.starttls()
    s.login(me, passwd)
    s.sendmail(me, [you], msg.as_string())
    s.quit()

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

    s = smtplib.SMTP(smtp_server)
    s.starttls()
    s.login(sender, passwd)
    s.sendmail(sender, [destination], msg.as_string())
    s.quit()

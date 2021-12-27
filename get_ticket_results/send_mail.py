import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr

sender = 'xxx@sina.com'

receiver1 = 'xxx@qq.com'
receiver_list = [receiver1]
subject = '获取彩票结果'

smtp_server = 'smtp.sina.com'
smtp_port = 587
smtp = smtplib.SMTP(smtp_server, smtp_port)
smtp.starttls()

###登录邮箱账号
username = 'xxx@sina.com'
####授权码(此处需要填写授权码)
password = 'xxx'


def send_mail(content):
    msg = MIMEText(content, 'html', 'utf-8')
    msg['From'] = formataddr(["彩票结果查询", sender])
    msg['To'] = formataddr(["接收人", receiver1])
    msg['Subject'] = Header(subject, 'utf-8')
    smtp.login(username, password)
    smtp.sendmail(sender, receiver_list, msg.as_string())
    smtp.quit()

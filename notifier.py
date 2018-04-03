# -*- coding: utf-8 -*-
# @Author: Theo
# @Date:   2018-04-01 02:34:28
# @Last Modified by:   TheoLong
# @Last Modified time: 2018-04-03 01:20:54
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from personal_info import get_info

info = get_info()
username = info['username']
password = info['password']
toaddr = info['toaddr']

def updateEmail(things2Update, time):
    global username
    global password
    global toaddr

    fromaddr = username
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Updates on your LTC! "

    body = "On " + time + ", " + things2Update
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

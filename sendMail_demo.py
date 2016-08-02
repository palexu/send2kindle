# import os
# subject="convert"
# target=""
# content=""
# command="echo \""+content+"\" | mutt -s \""+subject+"\" \""+target+"\""
# os.system(command)

import smtplib
from email.mime.text import MIMEText

msg=MIMEText("The body of the eamil is here")

msg['Subject']="An Email Alert"
msg['From']="1098672878@qq.com"
msg['To']="cnxujunyu@gmail.com"

s=smtplib.SMTP_SSL('smtp.qq.com')
username="1098672878@qq.com"
password="soilocrxuuxvfijc"
s.login(username,password)
s.send_message(msg)
s.quit()
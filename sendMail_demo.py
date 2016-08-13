# import os
# subject="convert"
# target=""
# content=""
# command="echo \""+content+"\" | mutt -s \""+subject+"\" \""+target+"\""
# os.system(command)

import smtplib
from email.mime.text import MIMEText

def do(content):
	msg=MIMEText(content)

	msg['Subject']="An Email Alert"
	msg['From']="1098672878@qq.com"
	msg['To']="cnxujunyu@gmail.com"

	s=smtplib.SMTP_SSL('smtp.qq.com')
	s.login(username,password)
	s.send_message(msg)
	s.quit()
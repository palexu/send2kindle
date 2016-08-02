import os
import optparse
import smtplib

from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.Utils import formatdate

config = {}
config["smtp_host"] = ""
config["smtp_port"] = "25"
config["use_ssl"] = False
config["use_tls"] = False
config["username"] = ""
config["password"] = ""
config["kindle_email"] = "addr@free.kindle.com"
config["from_addr"] = ""

def main():
	global config
	
    # config commandline arguments
	parser = optparse.OptionParser("usage: %prog [options] file1 file2", version="%prog 1.1 by Jamie Wilson")
	parser.add_option("-c", "--convert", action="store_true", dest="convert", default=False, help="Convert to AZW")
	parser.add_option("-k", "--kindle", action="store", type="string", dest="kindle_email", default=config["kindle_email"], help="Kindle email address")
	parser.add_option("-s", "--sender", action="store", type="string", dest="sender_email", default=config["from_addr"], help="Sender email address")
    
	# split commandline into options (opts) and arguments (args) (arguments = files)
	opts, args = parser.parse_args()
    
	# make sure this is a valid Kindle email (@free.kindle.com or @kindle.com)
	if opts.kindle_email.lower().find("@kindle.cn") < 0 and opts.kindle_email.lower().find("@kindle.com") < 0:
		parser.error("%s is not a valid Kindle email address." % opts.kindle_email)
    
    # check files
	if len(args) < 1:
		parser.error("No files specified to send to Kindle device.")

	for f in args:
		if not os.path.isfile(f):
			print "Invalid file: %s" % f
    
    # MAIL IT
	msg = MIMEMultipart()
	msg["From"] = opts.sender_email
	msg["To"] = opts.kindle_email
	if opts.convert is True:
		msg["Subject"] = "Convert"
	else:
		msg["Subject"] = ""
	msg["Date"] = formatdate(localtime=True)
        
	fCount = 0
	for f in args:
		if os.path.isfile(f):
			fCount = fCount + 1
			part = MIMEBase('application', "octet-stream")
			part.set_payload(open(f, "rb").read())
			Encoders.encode_base64(part)
			part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
			msg.attach(part)
    
    # Connect to SMTP server
	if config["smtp_port"] == "":
		config["smtp_port"] = "25"
		
	if config["use_ssl"] is True:
		server = smtplib.SMTP_SSL(config["smtp_host"], config["smtp_port"])
	else:
		server = smtplib.SMTP(config["smtp_host"], config["smtp_port"])
	if config["username"] is not None and config["password"] is not None:
		try:
			server.login(config["username"], config["password"])
		except Exception, e:
			print "Error: %s" % str(e[0])
			exit()
	if config["use_tls"] is True and config["use_ssl"] is False:
		# don't try to use TLS if we're already using SSL
		server.starttls
		
	# Send file(s)
	try:
		server.sendmail(opts.sender_email, opts.kindle_email, msg.as_string())
		server.close()
		if fCount > 1:
			print "Sent %d files to %s." % (fCount, opts.kindle_email)
		else:
			print "Sent %d file to %s." % (fCount, opts.kindle_email)
	except Exception, e:
		print "Unable to send email. Error: %s" % str(e)
            
if __name__ == "__main__":
	main()
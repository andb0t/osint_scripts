"""Send an email to a target from itself."""
import json
import os
import smtplib
import sys


if len(sys.argv) > 1:
    secret_file = sys.argv[1]
else:
    secret_file = 'secret.json'
# get email settings
if os.path.exists(secret_file):
    with open(secret_file) as file:
        secret = json.load(file)
        _target_names = secret["target_names"]
        _target_emails = secret["target_emails"]
        _text = secret["text"]
        _subject = secret["subject"]
        _account = secret["mail_server"]["email"]
        _password = secret["mail_server"]["password"]
        _smtp_out = secret["mail_server"]["smtp_out"]
else:
    print('Secret file "{}" does not exist! Please '.format(secret_file) +
          'create it and put your mail info there')
    sys.exit()

# open connection to mail server
server = smtplib.SMTP(_smtp_out, 587)
server.login(_account, _password)
# send emails
for target, target_name in zip(_target_emails, _target_names):

    msg = ("Subject: {}\n".format(_subject)).encode() + \
          ("From: {} <{}>\n".format(target_name, target)).encode() + \
          b"\r\n" + \
          _text.encode()

    server.sendmail(_account, target, msg)
server.quit()

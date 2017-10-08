from zipfile import *
from io import *
from smtplib import SMTP_SSL
from email.mime.application import *
from email.mime.multipart import *
from os import environ
from datetime import *

def processMail(files):
    mz = addToZip(files)
    sendOutMail(mz)


def addToZip(files):
    mybuffer = BytesIO()
    with ZipFile(mybuffer, 'w', compression=ZIP_DEFLATED) as myzip:
        for f in files:
            myzip.writestr(f.file_name, f.ovpn_file)
        myzip.close()
    return mybuffer


def sendOutMail(zipfile):
    toadd = environ['MAIL_TO']
    fromadd = environ['MAIL_FROM']
    smtp_server = environ['MAIL_SMTP']
    smtp_pwd = environ['MAIL_PWD']

    smtp_user = fromadd.split('@')[0]

    timestp = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')

    msg = MIMEMultipart()
    msg['Subject'] = 'VPN Gate ' + timestp
    msg['From'] = fromadd
    msg['Bcc'] = toadd

    att = MIMEApplication(zipfile.getvalue())
    zipfile.close()
    att.add_header('Content-Disposition', 'attachment', filename='ovpn ' + timestp + '.zip')
    msg.attach(att)

    client = SMTP_SSL(smtp_server)
    client.login(smtp_user, smtp_pwd)
    client.send_message(msg)
    client.quit()




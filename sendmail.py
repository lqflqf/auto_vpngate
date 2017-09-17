from smtplib import SMTP, SMTP_SSL
from email.message import EmailMessage


toadd = 'avanti.lee@gmail.com'
fromadd = 'auto_vpngate@auto_vpngate.org'

msg = EmailMessage()
msg.set_content('this is a test mail')
msg['Subject'] = 'dummy mail'
msg['From'] = fromadd
msg['To'] = toadd

client = SMTP_SSL('smtp.gmail.com')
client.send_message(msg)
client.quit()








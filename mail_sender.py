import configuration
import io
import zipfile
import datetime
import email.mime.application
import email.mime.multipart
import smtplib


class MailSender:
    def __init__(self, config):
        self.__config__: configuration.Configuration = config

    @staticmethod
    def __zip__(files):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
            for file_name, file_data in files:
                zip_file.writestr(file_name, file_data)
            zip_file.close()
        return buffer

    def __send_mail__(self, file: io.BytesIO):
        smtp_user = self.__config__.smtp_user.split('@')[0]

        time_stamp = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime('%Y%m%d %H%M%S')

        msg = email.mime.multipart.MIMEMultipart()
        msg['Subject'] = 'VPN Gate ' + time_stamp
        msg['From'] = self.__config__.smtp_user
        msg['Bcc'] = ','.join(self.__config__.mail)

        att = email.mime.application.MIMEApplication(file.getvalue())
        # file.close()
        att.add_header('Content-Disposition', 'attachment', filename='ovpn ' + time_stamp + '.zip')
        msg.attach(att)

        client = smtplib.SMTP_SSL(self.__config__.smtp_server)
        client.login(smtp_user, self.__config__.smtp_pwd)
        client.send_message(msg)
        client.quit()

    def send_zip(self, files):
        self.__send_mail__(self.__zip__(files))

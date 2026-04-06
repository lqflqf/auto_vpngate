import datetime
import email.message
import io
import logging
import smtplib
import zipfile

import configuration

logger = logging.getLogger(__name__)


class MailSender:
    def __init__(self, config: configuration.Configuration):
        self._config = config

    @staticmethod
    def _zip(files: list[tuple[str, str]]) -> io.BytesIO:
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
            for file_name, file_data in files:
                zip_file.writestr(file_name, file_data)
        return buffer

    def _send_mail(self, file: io.BytesIO, mail_body: str) -> None:
        time_stamp = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d %H%M%S")

        msg = email.message.EmailMessage()
        msg["Subject"] = "VPN Gate " + time_stamp
        msg["From"] = self._config.smtp_user
        msg["To"] = "undisclosed-recipients:;"
        msg["Bcc"] = ",".join(self._config.mail)
        msg.set_content(mail_body, subtype="html")
        msg.add_attachment(
            file.getvalue(),
            maintype="application",
            subtype="zip",
            filename="ovpn " + time_stamp + ".zip",
        )

        with smtplib.SMTP_SSL(self._config.smtp_server) as client:
            client.login(self._config.smtp_user, self._config.smtp_pwd)
            client.send_message(msg)

    def send_zip(self, content: tuple[list[tuple[str, str]], str]) -> None:
        zipped = self._zip(content[0])
        self._send_mail(zipped, content[1])

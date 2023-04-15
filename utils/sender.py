import logging
import smtplib
from dataclasses import dataclass
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from smtplib import (
    SMTPAuthenticationError,
    SMTPDataError,
    SMTPSenderRefused,
    SMTPServerDisconnected,
)

EMAIL_SENDING_ERRORS = (
    SMTPAuthenticationError,
    SMTPDataError,
    SMTPDataError,
    SMTPServerDisconnected,
    SMTPSenderRefused,
)


@dataclass()
class EmailSender:
    sender: str
    password: str
    display_name: str
    subject: str
    smtp_server: str = "smtp.yandex.ru"
    smtp_port: int = 465

    def _get_email_message(
        self,
        *,
        to_email: str,
        subject: str,
        attachments: list[str],
        contents,
    ) -> str:
        message = MIMEMultipart("mixed")
        message["From"] = "{contact} <{sender}>".format(
            contact=self.display_name, sender=self.sender
        )
        message["To"] = to_email
        message["CC"] = to_email
        message["Subject"] = subject
        body = MIMEText(contents, "html")
        message.attach(body)
        for file_path in attachments:
            file_path: Path = Path(file_path)
            with open(file_path, "rb") as file:
                attachment = MIMEApplication(
                    file.read(),
                )

                attachment.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=file_path.name.replace(" ", ""),
                )
                message.attach(attachment)

        return message.as_string()

    def __call__(
        self,
        *,
        to_email: str,
        attachments: list[str],
        contents,
    ) -> bool:
        try:
            msg_full = self._get_email_message(
                to_email=to_email,
                subject=self.subject,
                attachments=attachments,
                contents=contents,
            )

            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.sender, self.password)
                server.sendmail(self.sender, to_email, msg_full)
                server.quit()
            return True

        except EMAIL_SENDING_ERRORS as ex:
            logging.exception(f"Everything is bad:{ex}")
            return False

import yagmail
from yagmail.error import YagInvalidEmailAddress, YagConnectionClosed, YagAddressError
import smtplib


def send_email(to_email, subject, contents, attachments,
               smtp_server, smtp_port, email_sender,
               email_display_name, email_password):
    try:
        yag = yagmail.SMTP(user={email_sender: email_display_name},
                           password=email_password,
                           smtp_ssl=True,
                           host=smtp_server,
                           port=int(smtp_port))
        yag.send(to=to_email, subject=subject,
                 contents=contents, attachments=attachments)
        return True
    except (YagInvalidEmailAddress, YagConnectionClosed, smtplib.SMTPAuthenticationError,
            YagAddressError, smtplib.SMTPDataError, smtplib.SMTPServerDisconnected) as ex:
        return False

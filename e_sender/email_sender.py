import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import config


def send_mail(to_address: str):
    mail_message = MIMEMultipart()
    mail_message['From'] = config.ADMIN_EMAIL
    mail_message['To'] = to_address
    mail_message['Subject'] = 'Статистика на свадьбу'
    with open(config.FILE_NAME_STATIC, 'rb') as file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={config.FILE_NAME_STATIC}')
    mail_message.attach(part)
    try:
        with smtplib.SMTP('smtp.mail.ru', 587) as email_client:
            email_client.starttls()
            email_client.login(config.ADMIN_EMAIL, password=config.ADMIN_EMAIL_PASSWORD)
            email_client.send_message(mail_message)
            email_client.close()
            return True
    except:
        return False

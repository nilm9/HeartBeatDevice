import smtplib
from email.mime.text import MIMEText


def send_email_notification(to_email, subject, body):
    from_email = "your_email@example.com"
    from_password = "your_password"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.example.com', 465) as server:
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())

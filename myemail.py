import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests


def send_gmail(SUBJECT, BODY, TO, FROM):
    mail_from = "myProphet67@gmail.com"
    HEADER = """
    <head>
        <meta http-equiv="Content-Type" content="text/html"; charset = utf-8">
    </head>
    <body style="background-color:#ccffff;color:#003300"> 
        <h1 style="color:#006600;">EF not moving!</h1>
        <b>Check it out    
    """
    TAIL = """
            <i style="color:red">
    </body>
    """
    BODY = HEADER + '<br>'.join(BODY) + TAIL

    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = SUBJECT
    MESSAGE['To'] = TO
    MESSAGE['From'] = FROM

    HTML_BODY = MIMEText(BODY, 'html')
    MESSAGE.attach(HTML_BODY)
    PSD = "prophet67"

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(mail_from, PSD)
    server.sendmail(mail_from, [TO], MESSAGE.as_string())
    server.quit()

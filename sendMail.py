from email import message
import smtplib 
from email.mime.text import MIMEText

def sendMailFeedback(professor, subject, rating, comments):
    port = 2525
    smtpServer = 'smtp.mailtrap.io'
    login = '34bf4450240fee'
    password = '712ee21ae53aed'
    message = f'<h3> New feedback submission </h3>\
        <ul>\
            <li> Professor: {professor} </li>\
            <li> Subject: {subject} </li>\
            <li> Rating: {rating} </li>\
            <li> Comments: {comments} </li>\
        </ul>'
    senderEmail = 'senderEmail@example.com'
    recieverEmail = 'recieverEmail@gmail.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Professor feedback'
    msg['From'] = senderEmail
    msg['To'] = recieverEmail

    with smtplib.SMTP(smtpServer, port) as server:
        server.login(login, password)
        server.sendmail(senderEmail, recieverEmail, msg.as_string())

def sendMailRegister(username):
    port = 2525
    smtpServer = 'smtp.mailtrap.io'
    login = '34bf4450240fee'
    password = '712ee21ae53aed'
    message = f'<h3> You have successfully been registered! </h3>\
        <ul>\
            <li> Username: {username} </li>\
        </ul>'
    senderEmail = 'senderEmail@example.com'
    recieverEmail = 'recieverEmail@gmail.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Professor feedback'
    msg['From'] = senderEmail
    msg['To'] = recieverEmail

    with smtplib.SMTP(smtpServer, port) as server:
        server.login(login, password)
        server.sendmail(senderEmail, recieverEmail, msg.as_string())
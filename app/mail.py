import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_message(user_mail, text):
    msg = MIMEMultipart()

    receiver = user_mail
    message = f"Вы записаны на событие {text[2]} на время {text[1]}"

    msg.attach(MIMEText(message, 'plain'))
    msg["Subject"] = "Информация о вашем бронировании"

    server = smtplib.SMTP('smtp.mail.ru: 25')
    server.starttls()
    sender = "blatata2002@bk.ru"
    password = "NWeSgN9Ebz5hGPirus7P"
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()
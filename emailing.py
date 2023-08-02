import smtplib
import imghdr #gives you meta data about images
from email.message import EmailMessage

password = 'rjucthbnaegxdwez'
EMAIL = 'emilyphaplerin@gmail.com'
RECEIEVER = 'emilyphaplerin@gmail.com'
def send_email(image_path):
    email_message = EmailMessage()
    email_message['Subject'] = 'New customer showed up!'
    email_message.set_content('Hey, we just saw a new customer!')

    #open in rb mode because it's an image
    with open(image_path, 'rb') as file:
        content = file.read()
    email_message.add_attachment(content, maintype='image', subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo() #start 
    gmail.starttls()
    gmail.login(EMAIL, password)
    gmail.sendmail(EMAIL, RECEIEVER, email_message.as_string())
    gmail.quit()


if __name__ == '__main__':
    send_email(image_path='images/19.png') #choose a path that exists in your project 





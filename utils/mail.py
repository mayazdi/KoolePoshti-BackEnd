import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_otp_email(receiver_mail, receiver_name, otp_numbers):
    access_token = 'xwraarzgnszffddq'
    sender_mail = "yazdi.mohammad99@gmail.com"
    receiver_mail = "amin.yazdi@atrovan.com"

    smtp_host = 'smtp.gmail.com'
    smtp_port = 465

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Email verification"
    msg['From'] = sender_mail
    msg['To'] = receiver_mail

    text_content = "تایید ورود به کوله پشتی \n سلام، {} گرامی؛ \n ثبت نام اولیه برای ایمیل شما در سامانه کوله پشتی انجام شد. برای تایید ایمیل خود رمز عبور یک بار مصرف زیر را در فرایند ثبت نام خود وارد نمایید. \n {} \n در صورتی که شما درخواستی برای ورود به سامانه کوله پشتی نداشتید، این پیام را نادیده بگیرید. \n کوله پشتی © 1400 -"
    html_content = """\
    <html>
      <div style="font-family:vazir; margin-left:10%; margin-right:10%;border-style: solid; padding:10px;" dir="rtl">
        <h1>تایید ورود به کوله پشتی</h1>
        <b>
            سلام، {} گرامی؛
        </b>
        <p>
        ثبت نام اولیه برای ایمیل شما در سامانه کوله پشتی انجام شد.
        برای تایید ایمیل خود رمز عبور یک بار مصرف زیر را در فرایند ثبت نام خود وارد نمایید.
        </p>
        <div dir="ltr" style="text-align: center">
            <u><h2 style="display: inline;">{}</h3></u>
            <u><h2 style="display: inline;">{}</h3></u>
            <u><h2 style="display: inline;">{}</h3></u>
            <u><h2 style="display: inline;">{}</h3></u>
            <u><h2 style="display: inline;">{}</h3></u>
        </div>
        <p>
            در صورتی که شما درخواستی برای ورود به سامانه کوله پشتی نداشتید، این پیام را نادیده بگیرید.
        </p>
        <center>
            <a href="#" >کوله پشتی</a>
            &copy;
            1400 -
        </center>
        </div>
    </html>
    """

    part1 = MIMEText(text_content.format(receiver_name, otp_numbers), 'plain')
    part2 = MIMEText(html_content.format(receiver_name, otp_numbers[0], otp_numbers[1], otp_numbers[2], otp_numbers[3], otp_numbers[4]), 'html')

    msg.attach(part1)
    msg.attach(part2)

    try:
        server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        server.ehlo()
        server.login(sender_mail, access_token)
        server.sendmail(sender_mail, receiver_mail, msg.as_string())
        server.close()
        print('Email sent!')
        return True
    except:
        print('Something went wrong...')
        return False

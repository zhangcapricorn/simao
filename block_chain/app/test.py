import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

if __name__ == "__main__":
    sender = 'liudiyuhan1@163.com'
    password = '851102ldyh*'
    receivers = ';'.join(["zhangqiannan@dangdang.com", '408621756@qq.com'])
    msg = MIMEMultipart()
    msg['Subject'] = 'img'
    msg['From'] = sender
    msg['To'] = receivers

    file = "list.png"
    jpgpart = MIMEApplication(open("../result/%s" % file, 'rb').read())
    jpgpart.add_header('Content-Disposition', 'attachment', filename=file)
    msg.attach(jpgpart)

    client = smtplib.SMTP()
    client.connect('smtp.163.com', 465)
    client.starttls()
    client.login(sender, password)
    client.sendmail(sender, receivers, msg.as_string())
    client.quit()

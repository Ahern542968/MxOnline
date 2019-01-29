import random
import string

from MxOnline.settings import EMAIL_FROM
from django.core.mail import send_mail

from users.models import EmailVerifyRecode


def random_captcha(ramdom_length):
    captcha = ''.join(random.sample(string.ascii_letters + string.digits, ramdom_length))
    return captcha


def send_email(email, send_type):
    captcha = ''
    if send_type == 'register' or send_type == 'forget':
        captcha = random_captcha(16)
    elif send_type == 'update_email':
        captcha = random_captcha(4)
    email_recode = EmailVerifyRecode(email=email, send_type=send_type, captcha=captcha)
    email_recode.save()
    subject = ''
    message = ''
    if send_type == 'register':
        subject = 'python学习平台注册链接'
        message = '以下是python学习平台注册链接，请点击激活:http://127.0.0.1:8000/active/{0}'.format(captcha)
    elif send_type == 'forget':
        subject = 'python学习平台忘记密码'
        message = "请点击下面的链接找回你的密码: http://127.0.0.1:8000/reset/{0}".format(captcha)
    elif send_type == 'update_email':
        subject = 'python学习平台修改邮箱'
        message = "你的邮箱验证码为: {0}".format(captcha)
    send_mail(subject, message, EMAIL_FROM, [email], fail_silently=False)


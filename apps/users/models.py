from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=30, null=True, blank=True, verbose_name='昵称')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生年月')
    gender = models.CharField(max_length=6, choices=(('male', '男'), ('female', '女')), null=True, blank=True,
                              verbose_name='性别')
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name='地址')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号码')
    is_active = models.BooleanField(default=False, verbose_name='是否激活')
    image = models.ImageField(max_length=100, upload_to='image/%Y/%m', default='image/default.png', verbose_name='头像')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecode(models.Model):
    captcha = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(max_length=20, choices=(('register', '注册'), ('forget', '忘记密码'), ('update_email', '修改邮箱')), verbose_name='类型')
    send_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.email, self.captcha)


class Banner(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    image = models.ImageField(max_length=100, upload_to='banner/%Y/%m', verbose_name='轮播图')
    url = models.URLField(max_length=200, verbose_name='访问地址')
    index = models.IntegerField(default=100, verbose_name='顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='上传时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

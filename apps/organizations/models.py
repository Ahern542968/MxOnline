from datetime import datetime

from django.db import models


# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='城市名')
    desc = models.CharField(max_length=300, null=True, blank=True, verbose_name='描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Organization(models.Model):
    city = models.ForeignKey(City, verbose_name='所属城市', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='机构名')
    desc = models.CharField(max_length=300, null=True, blank=True, verbose_name='描述')
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name='地址')
    category = models.CharField(max_length=2, choices=(('jg', '机构'), ('gx', '高校'), ('gr', '个人')), null=True,
                                blank=True, verbose_name='类别')
    fav_num = models.IntegerField(default=0, verbose_name='收藏人数')
    click_num = models.IntegerField(default=0, verbose_name='点击人数')
    student_num = models.IntegerField(default=0, verbose_name='学习人数')
    course_num = models.IntegerField(default=0, verbose_name='课程数')
    tag = models.CharField(max_length=10, default='全国知名', null=True, blank=True, verbose_name='标签')
    image = models.ImageField(max_length=100, upload_to='org/%Y/%m', verbose_name='封面图')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    def get_teacher_num(self):
        teacher_num = self.teacher_set.all().count()
        return teacher_num

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(models.Model):
    organization = models.ForeignKey(Organization, verbose_name='所属机构', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='教师名')
    age = models.IntegerField(default=25, null=True, blank=True, verbose_name='年龄')
    desc = models.CharField(max_length=300, null=True, blank=True, verbose_name='描述')
    points = models.CharField(max_length=50, null=True, blank=True, verbose_name='教学特点')
    work_company = models.CharField(max_length=300, null=True, blank=True, verbose_name='公司')
    work_position = models.CharField(max_length=300, null=True, blank=True, verbose_name='职位')
    work_time = models.IntegerField(default=0, verbose_name='工作年限')
    fav_num = models.IntegerField(default=0, verbose_name='收藏人数')
    click_num = models.IntegerField(default=0, verbose_name='点击人数')
    image = models.ImageField(default=100, upload_to='teacher/%Y/%m', null=True, blank=True, verbose_name='头像')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    def get_course_num(self):
        course_num = self.course_set.all().count()
        return course_num

    class Meta:
        verbose_name = '讲师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

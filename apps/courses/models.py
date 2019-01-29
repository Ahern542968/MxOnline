from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

from organizations.models import Organization, Teacher
# Create your models here.


class Course(models.Model):
    orgration = models.ForeignKey(Organization, null=True, blank=True, verbose_name='所属机构', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, null=True, blank=True, verbose_name='讲师', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='课程名')
    desc = models.CharField(max_length=300, null=True, blank=True, verbose_name='描述')
    category = models.CharField(max_length=20, null=True, blank=True, verbose_name='课程类别')
    tag = models.CharField(max_length=10, null=True, blank=True, verbose_name='课程标签')
    detail = UEditorField(null=True, blank=True, verbose_name='详情', width=600, height=300, imagePath="course/ueditor/",
                          filePath="course/ueditor/")
    degree = models.CharField(max_length=2, choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), verbose_name='难度')
    youneed_know = models.CharField(max_length=300, null=True, blank=True, verbose_name='课程须知')
    teacher_tell = models.CharField(max_length=300, null=True, blank=True, verbose_name='老师告诉你')
    learn_time = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    stu_num = models.IntegerField(default=0, verbose_name='学习人数')
    fav_num = models.IntegerField(default=0, verbose_name='收藏人数')
    click_num = models.IntegerField(default=0, verbose_name='点击人数')
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')
    image = models.ImageField(max_length=100, upload_to='courses/%Y/%m', null=True, blank=True, verbose_name='封面图')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='发布时间')

    def get_lesson_num(self):
        lesson_num = self.lesson_set.all().count()
        return lesson_num
    get_lesson_num.short_description = '章节数'

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe('<a href="http://www.baidu.com/">跳转</>')
    go_to.short_description = '跳转'

    def get_learn_user(self):
        learn_user = self.usercourse_set.all()[:5]
        return learn_user

    def get_lesson(self):
        all_lesson = self.lesson_set.all()
        return all_lesson

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程名', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='发布时间')

    def get_video(self):
        all_video = self.video_set.all()
        return all_video

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节名', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='视频名')
    learn_time = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    url = models.CharField(max_length=200, null=True, blank=True, verbose_name='视频链接')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='发布时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程名', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='资源名')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name='下载链接')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='发布时间')

    class Meta:
        verbose_name = '资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

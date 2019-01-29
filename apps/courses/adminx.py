import xadmin

from .models import Course, Lesson, Video, CourseResource, BannerCourse
from organizations.models import Organization


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'degree', 'learn_time', 'detail', 'stu_num', 'fav_num', 'click_num', 'image',
                    'add_time', 'get_lesson_num', 'go_to']
    search_fields = ['name', 'desc', 'degree', 'learn_time', 'detail', 'stu_num', 'fav_num', 'click_num', 'image']
    list_filter = ['name', 'desc', 'degree', 'learn_time', 'detail', 'stu_num', 'fav_num', 'click_num', 'image',
                   'add_time']
    ordering = ['-click_num']
    readonly_fields = ['click_num', 'fav_num']
    exclude = ['stu_num']
    inlines = [LessonInline, CourseResourceInline]
    list_editable = ['desc', 'degree']
    refresh_times = [3, 5]
    style_fields = {'detail': 'ueditor'}
    import_excel = True

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        # 在保存课程时候统计课程数
        obj = self.new_obj
        obj.save()
        if obj.orgration is not None:
            orgration = obj.orgration
            orgration.course_num = Course.objects.filter(orgration=orgration).count()
            orgration.save()

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'degree','learn_time', 'detail', 'stu_num', 'fav_num', 'click_num', 'image',
                    'add_time']
    search_fields = ['name', 'desc', 'degree','learn_time', 'detail', 'stu_num', 'fav_num', 'click_num', 'image']
    list_filter = ['name', 'desc', 'degree','learn_time', 'detail', 'stu_num', 'fav_num', 'click_num', 'image',
                   'add_time']
    ordering = ['-click_num']
    readonly_fields = ['click_num', 'fav_num']
    exclude = ['stu_num']
    inlines = [LessonInline, CourseResourceInline]
    style_fields = {'detail': 'ueditor'}

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)

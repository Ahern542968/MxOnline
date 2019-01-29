from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse
from django.db.models import Q
from pure_pagination import Paginator, PageNotAnInteger

from .models import Course, Video
from operations.models import UserFavorite, UserCourse, UserComments
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_course = Course.objects.all()
        hot_course = all_course.order_by('-click_num')[:2]
        sort = request.GET.get('sort', '')
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_course = all_course.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords) |
                                           Q(degree__icontains=keywords))
        if sort:
            if sort == 'hot':
                all_course = all_course.order_by('-click_num')
            elif sort == 'students':
                all_course = all_course.order_by('-stu_num')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_course, 6, request=request)
        all_course = p.page(page)
        return render(request, 'course-list.html', {
            'all_course': all_course,
            'hot_course': hot_course,
            'sort': sort
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        has_fav_course = False
        has_fav_org = False
        course.click_num += 1
        course.save()
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(fav_id=course_id, fav_type=1).exists():
                has_fav_course = True
            if UserFavorite.objects.filter(fav_id=course.orgration.id, fav_type=2).exists():
                has_fav_org = True
        tag = course.tag
        if tag:
            relate_course = Course.objects.exclude(id=course_id).filter(tag=tag)[:2]
        else:
            relate_course = []
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_course': relate_course,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        user_course, created = UserCourse.objects.get_or_create(user=request.user, course=course)
        if created:
            course.stu_num += 1
            user_course.save()
        usercourses = course.usercourse_set.all()
        user_ids = [usercourse.user.id for usercourse in usercourses]
        usercourses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [usercourse.course.id for usercourse in usercourses]
        relate_course = Course.objects.filter(id__in=course_ids).exclude(id=course.id).order_by('-click_num')[:3]
        all_resource = course.courseresource_set.all()[:3]
        return render(request, 'course-video.html', {
            'course': course,
            'all_resource': all_resource,
            'relate_course': relate_course
        })


class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        usercourses = course.usercourse_set.all()
        user_ids = [usercourse.user.id for usercourse in usercourses]
        usercourses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [usercourse.course.id for usercourse in usercourses]
        relate_course = Course.objects.filter(id__in=course_ids).exclude(id=course.id).order_by('-click_num')[:3]
        all_resource = course.courseresource_set.all()[:3]
        comments = UserComments.objects.filter(course=course)[:10]
        return render(request, 'course-comment.html', {
            'course': course,
            'comments': comments,
            'relate_course': relate_course,
            'all_resource': all_resource
        })


class AddCommentView(View):
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({
                'status': 'fail',
                'msg': '用户未登录'
            })
        course_id = request.GET.get('course_id', 0)
        comment = request.GET.get('comments', '')
        if course_id > 0 and comment:
            course = Course.objects.get(id=course_id)
            user_comment = UserComments(course=course, user=user, comment=comment)
            user_comment.save()
            return JsonResponse({
                'status': 'success',
                'msg': '评论成功'
            })
        else:
            return JsonResponse({
                'status': 'fail',
                'msg': '评论失败'
            })


class VideoPlayView(LoginRequiredMixin, View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        user_course, created = UserCourse.objects.get_or_create(user=request.user, course=course)
        if created:
            user_course.save()
        usercourses = course.usercourse_set.all()
        user_ids = [usercourse.user.id for usercourse in usercourses]
        usercourses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [usercourse.course.id for usercourse in usercourses]
        relate_course = Course.objects.filter(id__in=course_ids).exclude(id=course.id).order_by('-click_num')[:3]
        all_resource = course.courseresource_set.all()[:3]
        return render(request, 'course-play.html', {
            'video': video,
            'course': course,
            'relate_course': relate_course,
            'all_resource': all_resource
        })
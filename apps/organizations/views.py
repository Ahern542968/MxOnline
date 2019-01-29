from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from pure_pagination import Paginator, PageNotAnInteger

from .forms import UserAskForm
from .models import Organization, Teacher, City
from operations.models import UserFavorite
from courses.models import Course
# Create your views here.


class OrgListView(View):
    def get(self, request):
        all_city = City.objects.all()
        all_org = Organization.objects.all()
        hot_org = all_org.order_by('-click_num')[:3]
        city_name = request.GET.get('city', '')
        ct_name = request.GET.get('ct', '')
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_org = all_org.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords))
        sort = request.GET.get('sort', '')
        if city_name:
            all_org = all_org.filter(city__name=city_name)
        if ct_name:
            all_org = all_org.filter(category=ct_name)
        if sort:
            if sort == 'students':
                all_org = all_org.order_by('-student_num')
            elif sort == 'courses':
                all_org = all_org.order_by('-course_num')
        org_num = all_org.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_org, 10, request=request)
        all_org = p.page(page)
        return render(request, 'org-list.html', {
            'all_city': all_city,
            'all_org': all_org,
            'hot_org': hot_org,
            'city_name': city_name,
            'ct_name': ct_name,
            'org_num': org_num,
            'sort': sort
        })


class UserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save()
            HttpResponse("{'status': 'success'}", content_type='application/json')
            # return JsonResponse({'status': 'success'})
        else:
            HttpResponse("{'status': 'success', 'msg': '添加出错'}", content_type='application/json')
            # return JsonResponse({'status': 'fail', 'msg': '添加错误'})


class OrgHomeView(View):
    def get(self, request, org_id):
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2).exists():
                has_fav = True
        org = Organization.objects.get(id=org_id)
        org.click_num += 1
        org.save()
        all_course = org.course_set.all()[:4]
        all_teacher = org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'org': org,
            'all_course': all_course,
            'all_teacher': all_teacher,
            'current_page': 'org_home',
            'has_fav': has_fav
        })


class OrgCourseView(View):
    def get(self, request, org_id):
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2).exists():
                has_fav = True
        org = Organization.objects.get(id=org_id)
        all_course = org.course_set.all()[:3]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_course, 1, request=request)
        all_course = p.page(page)
        return render(request, 'org-detail-course.html', {
            'org': org,
            'all_course': all_course,
            'current_page': 'org_course',
            'has_fav': has_fav
        })


class OrgDescView(View):
    def get(self, request, org_id):
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2).exists():
                has_fav = True
        org = Organization.objects.get(id=org_id)
        return render(request, 'org-detail-desc.html', {
            'org': org,
            'current_page': 'org_desc',
            'has_fav': has_fav
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2).exists():
                has_fav = True
        org = Organization.objects.get(id=org_id)
        all_teacher = org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'org': org,
            'all_teacher': all_teacher,
            'current_page': 'org_teacher',
            'has_fav': has_fav
        })


class AddFavView(View):
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({
                'status': 'fail',
                'msg': '用户未登录',
            })
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        user_fav = UserFavorite.objects.filter(user=user, fav_id=fav_id, fav_type=fav_type)
        if user_fav.exists():
            # 收藏记录已存在
            user_fav.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_num -= 1
                if course.fav_num < 0:
                    course.fav_num = 0
                course.save()
            elif int(fav_type) == 2:
                org = Organization.objects.get(id=int(fav_id))
                org.fav_num -= 1
                if org.fav_num < 0:
                    org.fav_num = 0
                org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_num -= 1
                if teacher.fav_num < 0:
                    teacher.fav_num = 0
                teacher.save()
            return JsonResponse({
                'status': 'success',
                'msg': '收藏',
            })
        else:
            if int(fav_type) > 0 and int(fav_id) > 0:
                user_fav = UserFavorite(user=user, fav_id=int(fav_id), fav_type=int(fav_type))
                user_fav.save()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_num += 1
                    if course.fav_num < 0:
                        course.fav_num = 0
                    course.save()
                elif int(fav_type) == 2:
                    org = Organization.objects.get(id=int(fav_id))
                    org.fav_num += 1
                    if org.fav_num < 0:
                        org.fav_num = 0
                    org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_num += 1
                    if teacher.fav_num < 0:
                        teacher.fav_num = 0
                    teacher.save()
                return JsonResponse({
                    'status': 'success',
                    'msg': '已收藏'
                })
            else:
                return JsonResponse({
                    'status': 'fail',
                    'msg': '收藏出错'
                })


class TeacherListView(View):
    def get(self, request):
        all_teacher = Teacher.objects.all()
        teacher_num = all_teacher.count()
        sort = request.GET.get('sort', '')
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_teacher = all_teacher.filter(name__icontains=keywords)
        if sort:
            if sort == 'hot':
                all_teacher = all_teacher.order_by('-click_num')
        sorted_teacher = all_teacher.order_by('-click_num')[:3]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teacher, 2, request=request)
        all_teacher = p.page(page)
        return render(request, 'teachers-list.html', {
            'all_teacher': all_teacher,
            'teacher_num': teacher_num,
            'sorted_teacher': sorted_teacher,
            'sort': sort
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        sorted_teacher = Teacher.objects.all().order_by('-click_num')[:3]
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_num += 1
        teacher.save()
        all_course = teacher.course_set.all()
        has_org_fav = False
        has_teacher_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id).exists():
            has_teacher_fav = True
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.organization.id).exists():
            has_org_fav = True
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_course, 3, request=request)
        all_course = p.page(page)
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'sorted_teacher': sorted_teacher,
            'all_course': all_course,
            'has_teacher_fav': has_teacher_fav,
            'has_org_fav': has_org_fav
        })

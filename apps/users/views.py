from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import render_to_response
from pure_pagination import Paginator, PageNotAnInteger

from operations.models import UserCourse, UserFavorite, UserMsg
from organizations.models import Organization, Teacher
from courses.models import Course
from .models import UserProfile, EmailVerifyRecode, Banner
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UploadImageForm, UpdateInfoForm
from utils.send_email import send_email
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.filter(Q(username=username) | Q(email=username))
            if user is not None:
                if user.check_password(password=password):
                    return user
                else:
                    return None
            else:
                return None
        except ObjectDoesNotExist:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    redirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['email']
            if UserProfile.objects.filter(Q(username=username) | Q(email=username)).exists():
                return render(request, 'register.html', {'msg': '用户已存在'})
            password = register_form.cleaned_data['password']
            user_profile = UserProfile.objects.create_user(username=username, email=username, password=password)
            user_profile.save()
            send_email(username, 'register')
            return render(request, 'login.html', {})
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_recode = EmailVerifyRecode.objects.filter(captcha=active_code)
        if all_recode.exists():
            for recode in all_recode:
                email = recode.email
                user_profile = UserProfile.objects.get(email=email)
                user_profile.is_active = True
                user_profile.save()
                recode.delete()
        else:
            return render(request, 'active_fail.html', {'msg': '激活链接失效'})


class ForgetPwdView(View):
    def get(self, request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form})

    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = forgetpwd_form.cleaned_data['email']
            send_email(email, 'forget')
            return render(request, 'send_success.html', {})
        return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form})


class ResetPwdView(View):
    def get(self, request, active_code):
        all_recode = EmailVerifyRecode.objects.filter(captcha=active_code)
        if all_recode.exists():
            for recode in all_recode:
                email = recode.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html', {'msg': '激活链接失效'})


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            email = request.POST.get('email')
            password = modify_form.cleaned_data['password']
            user = UserProfile.objects.get(email=email)
            user.set_password(password)
            user.save()
            return render(request, 'login.html', {})
        else:
            email = request.POST.get('email')
            return render(request, 'password_reset.html', {'modify_form': modify_form, 'email': email})


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        update_info_form = UpdateInfoForm(request.POST, instance=request.user)
        if update_info_form.is_valid():
            update_info_form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail'})


class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail'})


class UpdatePwdView(LoginRequiredMixin, View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            password = modify_form.cleaned_data['password']
            request.user.set_password(password)
            request.user.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '密码不一致'})


class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email).exists():
            return JsonResponse({'status': 'fail', 'msg': '邮箱已存在'})
        send_email(email, 'update_email')
        return JsonResponse({'status': 'success'})


class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email', '')
        captcha = request.POST.get('captcha', '')
        email_recode = EmailVerifyRecode.objects.filter(email=email, send_type='update_email', captcha=captcha)
        if email_recode:
            request.user.email = email
            request.user.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'email': '验证码无效'})


class UserCourseView(LoginRequiredMixin, View):
    def get(self, request):
        all_usercourse = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'all_usercourse': all_usercourse
        })


class UserFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type='2')
        all_org = []
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = Organization.objects.get(id=org_id)
            all_org.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'all_org': all_org
        })


class UserFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type='3')
        all_teacher = []
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            all_teacher.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'all_teacher': all_teacher
        })


class UserFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type='1')
        all_course = []
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            all_course.append(course)
        return render(request, 'usercenter-mycourse.html', {
            'all_course': all_course
        })


class UserMessageView(LoginRequiredMixin, View):
    def get(self, request):
        messages = UserMsg.objects.filter(user=request.user.id)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(messages, 2, request=request)
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'messages': messages
        })


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect(reverse('index'))


class IndexView(View):
    def get(self, request):
        all_banner = Banner.objects.all().order_by()[:3]
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        orgs = Organization.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banner': all_banner,
            'courses': courses,
            'banner_courses': banner_courses,
            'orgs': orgs
        })


def page_not_found(request):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response

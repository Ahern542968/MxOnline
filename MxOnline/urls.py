"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from MxOnline.settings import MEDIA_ROOT
import xadmin

from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetPwdView, ModifyPwdView, IndexView


urlpatterns = [
    path(r'xadmin/', xadmin.site.urls),
    path(r'^ueditor/',include('DjangoUeditor.urls')),
    re_path(r'media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    # re_path(r'static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT}),
    path(r'captcha/', include('captcha.urls')),
    path('', IndexView.as_view(), name='index'),
    path(r'login/', LoginView.as_view(), name='login'),
    path(r'register/', RegisterView.as_view(), name='register'),
    path(r'forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    path(r'modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),
    re_path(r'active/(?P<active_code>.*)/', ActiveUserView.as_view(), name='user_active'),
    re_path(r'reset/(?P<active_code>.*)/', ResetPwdView.as_view(), name='reset_pwd'),
    path(r'org/', include(('organizations.urls', 'organizations'), namespace='org')),
    path(r'course/', include(('courses.urls', 'courses'), namespace='course')),
    path(r'user/', include(('users.urls', 'users'), namespace='user')),
]

handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'

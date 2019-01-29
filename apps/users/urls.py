from django.urls import path

from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, UserCourseView
from .views import UserFavOrgView, UserFavTeacherView, UserFavCourseView, UserMessageView, LogoutView


urlpatterns = [
    path(r'user_info/', UserInfoView.as_view(), name='user_info'),
    path(r'image_upload/', UploadImageView.as_view(), name='image_upload'),
    path(r'update_pwd/', UpdatePwdView.as_view(), name='update_pwd'),
    path(r'sendemail_code/', SendEmailCodeView.as_view(), name='sendemail_code'),
    path(r'update_email/', UpdateEmailView.as_view(), name='update_email'),
    path(r'user_course/', UserCourseView.as_view(), name='user_course'),
    path(r'user_fav/org/', UserFavOrgView.as_view(), name='fav_org'),
    path(r'user_fav/teacher/', UserFavTeacherView.as_view(), name='fav_teacher'),
    path(r'user_fav/course/', UserFavCourseView.as_view(), name='fav_course'),
    path(r'user_message/', UserMessageView.as_view(), name='user_message'),
    path(r'logout/', LogoutView.as_view(), name='logout'),
]
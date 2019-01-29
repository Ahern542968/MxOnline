from django.urls import path

from .views import OrgListView, UserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView
from .views import TeacherListView, TeacherDetailView


urlpatterns = [
    path(r'org_list/', OrgListView.as_view(), name='org_list'),
    path(r'add_ask/', UserAskView.as_view(), name='add_ask'),
    path(r'add_fav/', AddFavView.as_view(), name='add_fav'),
    path(r'org_home/(?P<org_id>\d+)/', OrgHomeView.as_view(), name='org_home'),
    path(r'org_course/(?P<org_id>\d+)/', OrgCourseView.as_view(), name='org_course'),
    path(r'org_desc/(?P<org_id>\d+)/', OrgDescView.as_view(), name='org_desc'),
    path(r'org_teacher/(?P<org_id>\d+)/', OrgTeacherView.as_view(), name='org_teacher'),
    path(r'teacher/list/', TeacherListView.as_view(), name='teacher_list'),
    path(r'teacher/detail/(?P<teacher_id>\d+)/', TeacherDetailView.as_view(), name='teacher_detail'),
]
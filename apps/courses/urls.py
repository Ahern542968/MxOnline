from django.urls import path

from .views import CourseListView, CourseDetailView, CourseInfoView, AddCommentView, CourseCommentView, VideoPlayView

urlpatterns = [
    path(r'course_list/', CourseListView.as_view(), name='course_list'),
    path(r'course_detail/(?P<course_id>\d+)/', CourseDetailView.as_view(), name='course_detail'),
    path(r'info/(?P<course_id>\d+)/', CourseInfoView.as_view(), name='course_info'),
    path(r'comments/(?P<course_id>\d+)/', CourseCommentView.as_view(), name='course_comments'),
    path(r'video/(?P<video_id>\d+)/', VideoPlayView.as_view(), name='video_play'),
    path(r'add_comment/', AddCommentView.as_view(), name='add_comment'),
]
import xadmin

from .models import UserCourse, UserAsk, UserMsg, UserComments, UserFavorite


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user__username', 'course__name', 'add_time']


class UserAskAdmin(object):
    list_display = ['name', 'course', 'course', 'add_time']
    search_fields = ['name', 'course', 'course']
    list_filter = ['name', 'course', 'course', 'add_time']


class UserMsgAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']


class UserCommentsAdmin(object):
    list_display = ['course', 'user', 'comment', 'add_time']
    search_fields = ['course', 'user', 'comment']
    list_filter = ['course__name', 'user', 'comment', 'add_time']


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user__username', 'fav_id', 'fav_type', 'add_time']


xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserMsg, UserMsgAdmin)
xadmin.site.register(UserComments, UserCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)


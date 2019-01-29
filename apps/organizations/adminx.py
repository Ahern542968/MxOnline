import xadmin

from .models import City, Organization, Teacher


class CityAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class OrganizationAdmin(object):
    list_display = ['name', 'desc', 'city', 'address', 'fav_num', 'click_num', 'image', 'add_time']
    search_fields = ['name', 'desc', 'city', 'address', 'fav_num', 'click_num', 'image']
    list_filter = ['name', 'desc', 'city__name', 'address', 'fav_num', 'click_num', 'image', 'add_time']
    relfield_style = 'fk-ajax'


class TeacherAdmin(object):
    list_display = ['name', 'desc', 'organization', 'work_company', 'work_position', 'work_time', 'fav_num',
                    'click_num', 'points', 'add_time']
    search_fields = ['name', 'desc', 'organization', 'work_company', 'work_position', 'work_time', 'fav_num',
                     'click_num', 'points']
    list_filter = ['name', 'desc', 'organization__name', 'work_company', 'work_position', 'work_time', 'fav_num',
                   'click_num', 'points', 'add_time']


xadmin.site.register(City, CityAdmin)
xadmin.site.register(Organization, OrganizationAdmin)
xadmin.site.register(Teacher, TeacherAdmin)

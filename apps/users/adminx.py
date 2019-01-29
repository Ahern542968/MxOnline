import xadmin
from xadmin import views

from .models import EmailVerifyRecode, Banner


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = 'Python在线学习平台'
    site_footer = 'Python学习平台'
    menu_style = 'accordion'


class EmailVerifyRecodeAdmin(object):
    list_display = ['email', 'send_type', 'captcha', 'send_time']
    search_fields = ['email']
    list_filter = ['send_type', 'send_time']
    model_icon = 'fa fa-envelope-o'


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(EmailVerifyRecode, EmailVerifyRecodeAdmin)
xadmin.site.register(Banner, BannerAdmin)

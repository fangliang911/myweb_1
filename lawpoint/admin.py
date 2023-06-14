from django.contrib import admin
from .models import Lawpoint
# Register your models here.



class Lawpoint_admin(admin.ModelAdmin):
    # 详细页面字段
    fields = ('law_name', 'law_sub', 'law_point')
    # 设置页面可以展示的字段
    list_display = ('id','law_name', 'law_sub', 'law_point')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    # 设置过滤选项
    list_filter = ('law_name', 'law_sub',)
    # 每页显示条目数 缺省值100
    list_per_page = 50
    def has_edit_permission(self,request):
        # 禁用编辑
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Lawpoint,Lawpoint_admin)
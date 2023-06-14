from django.contrib import admin
from datetime import datetime
# Register your models here.
from .models import ChatMsg

class ChatMsg_admin(admin.ModelAdmin):
    # 详细页面字段
    fields = ('chat_datetime', 'chat_content')
    # 设置页面可以展示的字段
    list_display = ('id','chat_datetime', 'chat_content')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    # 设置过滤选项
    list_filter = ('chat_datetime',)
    # 每页显示条目数 缺省值100
    list_per_page = 100
    # show all页面上的model数目，缺省200
    # list_max_show_all = 200
    # 设置可编辑字段 如果设置了可以编辑字段，页面会自动增加保存按钮
    # list_editable = ('',)
    # 按日期月份筛选 该属性一般不用
    # date_hierarchy = 'CREATED_TIME'
    # 按发布日期降序排序
    ordering = ('-chat_datetime',)
    # 搜索条件设置
    search_fields = ('chat_datetime','chat_content',)
    def has_edit_permission(self,request):
        # 禁用编辑
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False





admin.site.register(ChatMsg,ChatMsg_admin)
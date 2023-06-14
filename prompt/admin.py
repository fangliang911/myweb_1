from django.contrib import admin
from datetime import datetime
from django.contrib.auth.models import User
# Register your models here.
from .models import Prompt_manage
from django.utils.safestring import mark_safe



class Prompt_admin(admin.ModelAdmin):
    # 详细页面字段
    fields = ('prompt_type', 'prompt_template')
    # 设置页面可以展示的字段
    list_display = ('id','prompt_type', 'prompt_template','create_user',# 'tochatgpt',
              'create_datetime','update_datetime')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    # list_display_links = ('prompt_template',)
    # 设置过滤选项
    list_filter = ('prompt_type', 'create_user',)
    # 每页显示条目数 缺省值100
    list_per_page = 100
    # show all页面上的model数目，缺省200
    # list_max_show_all = 200
    # 设置可编辑字段 如果设置了可以编辑字段，页面会自动增加保存按钮
    # list_editable = ('',)
    # 按日期月份筛选 该属性一般不用
    # date_hierarchy = 'CREATED_TIME'
    # 按发布日期降序排序
    ordering = ('-create_datetime',)
    # 搜索条件设置
    search_fields = ('prompt_type','prompt_template','create_user',)

    def save_model(self, request, obj, form, change):
        if change:
            obj.update_datetime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            super().save_model(request, obj, form, change)
        else:
            obj.create_user = request.user
            obj.create_datetime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            obj.update_datetime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            super().save_model(request, obj, form, change)

    # 自定义操作
    @admin.display(description='一键使用', ordering='prompt_type')
    def tochatgpt(self, obj):
        # 在新标签中打开修改界面，url可以随意指定。
        # 尝试失败，原因未知。
        data = '{"name": "法考应用", "icon": "fas fa-user-tie", "url": "/assistant/chat/" ,"newTab": 1}' # % (obj.prompt_type)
        btn = f"""<button οnclick='window.open("/assistant/chat/")'
                             class='el-button el-button--danger el-button--small'>tochatgpt</button>"""
        # btn =f"""<button οnclick='self.parent.app.opentab(...))'
        #                      class='el-button el-button--danger el-button--small'>复制</button>"""
        return mark_safe(f"<div>{btn}</div>")

admin.site.register(Prompt_manage,Prompt_admin)
admin.site.site_header = '法外狂徒基地'
admin.site.site_title = '法外狂徒基地'
admin.site.index_title = u'法外狂徒基地'
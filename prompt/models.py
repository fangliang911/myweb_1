from django.db import models
import django.utils.timezone as timezone
from django.contrib.auth.models import User


# Create your models here.
class Prompt_manage(models.Model):
    prompt_type = models.CharField(max_length=50, verbose_name="提示词分类")
    prompt_template = models.TextField(verbose_name="提示词模板")
    create_user = models.CharField(max_length=20)
    # create_user=models.ForeignKey(User,related_name="c_user")
    create_datetime = models.DateTimeField(verbose_name="创建时间", default=timezone.now)
    update_datetime = models.DateTimeField(verbose_name="更新时间", default=timezone.now)

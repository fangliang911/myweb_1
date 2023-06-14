from django.db import models
import django.utils.timezone as timezone
# Create your models here.
class ChatMsg(models.Model):
    chat_datetime = models.DateTimeField(verbose_name="会话时间", default=timezone.now)
    chat_content = models.TextField(verbose_name="完整对话")
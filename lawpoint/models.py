from django.db import models


# Create your models here.
class Lawpoint(models.Model):
    law_name = models.CharField(max_length=20, verbose_name="法律名称")
    law_sub = models.CharField(max_length=20, verbose_name="法律子项")
    law_point = models.CharField(max_length=50, verbose_name="法律考点")

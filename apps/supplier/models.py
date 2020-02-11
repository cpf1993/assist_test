from django.db import models

# Create your models here.
class log_search(models.Model):
    object_type = models.CharField(
        max_length=64,
        null=False, help_text='查询维度:SUPPLIER(30),LINK(60)，SKU_LINK_REL(20)')
    object_id = models.CharField(
        max_length=64, help_text='对象id'
    )
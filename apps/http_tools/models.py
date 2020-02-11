# coding=utf-8

from django.db import models

# Create your models here.
class Project(models.Model):
    project_name = models.CharField(max_length=64, help_text="项目名称")
    description = models.CharField(max_length=100, help_text="项目描述")
    responsible_name = models.CharField(max_length=64, help_text="负责人")
    create_time = models.DateTimeField(auto_now_add=True, help_text="创建时间")
    update_time = models.DateTimeField(auto_now=True, help_text="更新时间")

    class Meta:
        app_label = 'http_tools'
        db_table = "project"

    def __str__(self):
        return self.project_name


class HttpInterface(models.Model):
    title = models.CharField(max_length=64, help_text="工具名称")
    create_user = models.CharField(max_length=64, help_text="创建人")
    tool_note = models.TextField(blank=True, help_text="工具备注")
    url = models.CharField(max_length=256, help_text="接口url")
    method = models.CharField(max_length=10, help_text="请求方式")
    data_type = models.CharField(max_length=10, help_text="数据类型")
    request_header_param = models.TextField(help_text="请求头")
    request_body_param = models.TextField(help_text="请求体")
    create_time = models.DateTimeField(auto_now_add=True, help_text="创建时间")
    update_time = models.DateTimeField(auto_now=True, help_text="更新时间")
    project = models.ForeignKey(Project, related_name="project_http_interface", on_delete=models.PROTECT)

    class Meta:
        app_label = 'http_tools'
        db_table = "http_interface"

    def __str__(self):
        return self.title
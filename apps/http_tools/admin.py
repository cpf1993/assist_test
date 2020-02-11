# coding=utf-8

from django.contrib import admin
from .models import Project, HttpInterface

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'project_name', 'description', 'create_time', 'update_time']

admin.site.register(Project, ProjectAdmin)


class HttpInterfaceAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'create_user', 'tool_note', 'url', 'method', 'data_type', 'request_header_param',
        'request_body_param', 'create_time', 'update_time', 'project']

admin.site.register(HttpInterface, HttpInterfaceAdmin)
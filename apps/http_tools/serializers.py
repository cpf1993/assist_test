# coding=utf-8
from .models import Project, HttpInterface
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'project_name', 'responsible_name', 'create_time', 'update_time')
        model = Project

class ProjectDetailSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        fields = '__all__'
        model = Project


class HttpInterfaceSerializer(serializers.ModelSerializer):

    # 以下字段从其它表读取
    project_name = serializers.CharField()

    class Meta:
        fields = ('id', 'title', 'create_user', 'project', 'project_name', 'create_time', 'update_time')
        model = HttpInterface


class HttpInterfaceDetailSerializer(serializers.ModelSerializer):
    request_header_param = serializers.JSONField()
    request_body_param = serializers.JSONField()

    class Meta:
        fields = '__all__'
        model = HttpInterface

class ProjectAndInterfaceSerializer(serializers.ModelSerializer):

    # 以下字段从其它表读取
    tool_title_list = serializers.CharField()

    class Meta:
        fields = ('id', 'project_name', 'tool_title_list')
        model = Project



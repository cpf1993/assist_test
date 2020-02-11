# coding = utf-8

import django_filters
import rest_framework_filters as filters

from apps.http_tools.models import Project, HttpInterface

class ProjectFilter(django_filters.FilterSet):

    class Meta:
        model = Project
        fields = {
            'project_name': ['icontains']
        }



class HttpInterfaceFilter(django_filters.FilterSet):

    project_name = django_filters.CharFilter(field_name="project__project_name", lookup_expr='exact')

    class Meta:
        model = HttpInterface
        fields = {
            'title': ['icontains']
        }

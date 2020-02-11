# coding=utf-8
import json

from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic.base import View
from .models import Project, HttpInterface
from .serializers import ProjectSerializer, ProjectDetailSerializer, HttpInterfaceSerializer, HttpInterfaceDetailSerializer, ProjectAndInterfaceSerializer
from .service import get_project_and_interface, get_http_interface_info, run_http_interface, run_request
from apps.common.base import BaseViewSet, bad_request, http_json_response
from apps.http_tools.filters import ProjectFilter, HttpInterfaceFilter
from schema import Schema, And, Use, Optional, Or, SchemaError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.

class ProjectViewSet(BaseViewSet):
    # serializer_class = ProjectSerializer
    # queryset = Project.objects.all().order_by("create_time")
    queryset = Project.objects.all().order_by("-create_time")
    filter_backends = (DjangoFilterBackend,)
    filter_class = ProjectFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectSerializer
        if self.action in ['retrieve', 'create', 'update']:
            return ProjectDetailSerializer
        return ProjectSerializer

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        Schema(
            {
                'project_name': And(lambda a: len(a) <= 50 and len(a) > 0, error = u'名称为空或太长'),
                'responsible_name': And(lambda a: len(a) <= 20 and len(a) > 0, error= u'负责人名称为空或太长'),
                Optional('description'): Or('', lambda a: len(a) <= 100, error = u'描述太长')
            },
            ignore_extra_keys=True
        ).validate(request.data)

        return super(ProjectViewSet, self).create(request, *args, **kwargs)

    @csrf_exempt
    def update(self, request, *args, **kwargs):
        Schema(
            {
                'project_name': And(lambda a: len(a) <= 50 and len(a) > 0, error=u'名称为空或太长'),
                'responsible_name': And(lambda a: len(a) <= 20 and len(a) > 0, error=u'负责人名称为空或太长'),
                Optional('description'): Or('', lambda a: len(a) <= 100, error = u'描述太长')
            },
            ignore_extra_keys=True
        ).validate(request.data)

        return super(ProjectViewSet, self).update(request, *args, **kwargs)



class HttpInterfaceViewSet(BaseViewSet):
    queryset = HttpInterface.objects.all().extra(select={'project_name': 'project.project_name'},
                                                 tables=['project'],
                                                 where=['http_interface.project_id=project.id']
                                                 ).order_by('-create_time')
    filter_backends = (DjangoFilterBackend,)
    filter_class = HttpInterfaceFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return HttpInterfaceSerializer
        if self.action in ['create', 'update']:
            return HttpInterfaceDetailSerializer
        return HttpInterfaceSerializer

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        Schema(
            {
                'title': And(lambda a: len(a) <= 50 and len(a) > 0, error=u'名称为空或太长'),
                'create_user': And(lambda a: len(a) <= 20 and len(a) > 0, error=u'负责人为空或太长'),
                'tool_note': And(lambda a:len(a) > 0, error=u'工具备注不能为空'),
                'url': And(lambda a:len(a) <= 250 and len(a) > 0, error=u'url为空或太长'),
                'method': And(lambda a: a in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE'), error=u'请求方式错误'),
                'data_type': And(lambda a: a in ('json', 'data', 'params'), error=u'数据类型有误'),
                'request_header_param': And(lambda a: len(a) < 5000, error=u'请求头过长'),
                'request_body_param': And(lambda a: type(a) is list or type(a) is dict, error=u'请输入json格式'),
                'project': And(int, error=u'所选项目有误')
            },
            ignore_extra_keys=True
        ).validate(request.data)

        return super(HttpInterfaceViewSet, self).create(request, *args, **kwargs)

    @csrf_exempt
    def update(self, request, *args, **kwargs):
        Schema(
            {
                'title': And(lambda a: len(a) <= 50 and len(a) > 0, error=u'名称为空或太长'),
                'create_user': And(lambda a: len(a) <= 20 and len(a) > 0, error=u'负责人为空或太长'),
                'tool_note': And(lambda a: len(a) > 0, error=u'工具备注不能为空'),
                'url': And(lambda a: len(a) <= 250 and len(a) > 0, error=u'url为空或太长'),
                'method': And(lambda a: a in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE'), error=u'请求方式错误'),
                'data_type': And(lambda a: a in ('json', 'data', 'params'), error=u'数据类型有误'),
                'request_header_param': And(lambda a: len(a) < 5000, error=u'请求头过长'),
                'request_body_param': And(lambda a: type(a) is list or type(a) is dict, error=u'请输入json格式'),
                'project': And(int, error=u'所选项目有误')
            },
            ignore_extra_keys=True
        ).validate(request.data)

        return super(HttpInterfaceViewSet, self).update(request, *args, **kwargs)



class HttpInterfaceBasicInfoView(View):
    """
      获取接口工具的基本信息
    """

    def get(self, request):
        try:
            id = request.GET.get("id")
            if not id:
                raise bad_request(u"缺少id入参")
            http_interface_info = get_http_interface_info(id)
            return http_json_response(http_interface_info)
            # return json_resp(get_http_interface_info(id))
        except Exception as e:
            return bad_request(e)



# class ProjectAndInterfaceViewSet(BaseViewSet):
#     serializer_class = ProjectAndInterfaceSerializer
#     queryset = Project.objects.all().extra(select={'tool_title_list': 'http_interface.title'},
#                                            tables=['http_interface'],
#                                            where=['http_interface.project_id=project.id']
#                                            ).order_by('-create_time')
#     def list(self, request, *args, **kwargs):
#         response = super(ProjectAndInterfaceViewSet, self).list(request, args, kwargs)
#         return response
class ProjectAndInterfaceViewSet(BaseViewSet):

    def list(self, request, *args, **kwargs):
        response = get_project_and_interface()
        return response



class RunInterfaceByIdViewSet(View):
    """
    通过id运行接口
    """

    def get(self, request):
        try:
            id = request.GET.get("id")
            if not id:
                raise bad_request(u"该接口工具不存在")
            http_interface_res = run_http_interface(id)
            return http_json_response(http_interface_res)
        except Exception as e:
            return bad_request(e)


# @csrf_exempt不适用于基于通用视图的类
@method_decorator(csrf_exempt, name='dispatch')
class RunInterfaceByInputViewSet(View):
    """
    通过工具页面输入的参数，运行接口工具
    """

    def post(self, request):
        req = json.loads(request.body)
        try:
            Schema(
                {
                    'url': And(lambda a: len(a) <= 250 and len(a) > 0, error=u'url为空或太长'),
                    'method': And(lambda a: a in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE'), error=u'请求方式错误'),
                    'data_type': And(lambda a: a in ('json', 'data', 'params'), error=u'数据类型有误'),
                    'request_header_param': And(lambda a: len(a) < 5000, error=u'请求头过长'),
                    'request_body_param': And(lambda a: type(a) is list or type(a) is dict, error=u'请输入json格式'),
                },
            ignore_extra_keys=True
            ).validate(req)
        except SchemaError as e:
            return bad_request(str(e))

        url = req['url']
        method = req['method']
        data_type = req['data_type']
        headers = req['request_header_param']
        param_data = req['request_body_param']

        response = run_request(url=url, method=method, headers=headers, data_type=data_type, param_data=param_data)
        return http_json_response(response)




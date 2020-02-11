# coding=utf-8
import functools
import traceback
import logging
import json

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http.response import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder


logger = logging.getLogger(__name__)


def json_resp(func):
    @functools.wraps(func)
    def wrap_resp(*args, **kwargs):
        code, http_status, msg = 0, status.HTTP_200_OK, "OK"
        try:
            resp = func(*args, **kwargs)
            if isinstance(resp, Response):
                resp = resp.data
            elif isinstance(resp, HttpResponse):
                return resp

            if isinstance(resp, dict) and "code" in resp:
                code = resp["code"]
                msg = resp.get("msg", "CODE:{}".format(code))
                body = resp.get("body")
            else:
                body = resp

        except Exception as e:

            logger.error(traceback.format_exc())
            code, msg, body = 1, str(e), None

        json_data = {
            "code": code,
            "msg": msg,
            "body": body,
        }
        return Response(json_data, status=http_status)
        # return HttpResponse(
        #     json.dumps(json_data, cls=DjangoJSONEncoder),
        #     content_type='application/json', status=http_status)
    return wrap_resp


# 该Mixin使用 https://github.com/wimglenn/djangorestframework-queryfields
class QueryFieldsMixin(object):
    # If using Django filters in the API, these labels mustn't conflict with any model field names.
    include_arg_name = 'fields'
    exclude_arg_name = 'fields!'

    # Split field names by this string.  It doesn't necessarily have to be a single character.
    # Avoid RFC 1738 reserved characters i.e. ';', '/', '?', ':', '@', '=' and '&'
    delimiter = ','

    def __init__(self, *args, **kwargs):
        super(QueryFieldsMixin, self).__init__(*args, **kwargs)

        try:
            request = self.context['request']
            method = request.method
        except (AttributeError, TypeError, KeyError):
            # The serializer was not initialized with request context.
            return

        if method != 'GET':
            return

        try:
            query_params = request.query_params
        except AttributeError:
            # DRF 2
            query_params = getattr(request, 'QUERY_PARAMS', request.GET)

        includes = query_params.getlist(self.include_arg_name)
        include_field_names = {
            name for names in includes for name in names.split(self.delimiter) if name}

        excludes = query_params.getlist(self.exclude_arg_name)
        exclude_field_names = {
            name for names in excludes for name in names.split(self.delimiter) if name}

        if not include_field_names and not exclude_field_names:
            # No user fields filtering was requested, we have nothing to do here.
            return

        serializer_field_names = set(self.fields)

        fields_to_drop = serializer_field_names & exclude_field_names
        if include_field_names:
            fields_to_drop |= serializer_field_names - include_field_names

        for field in fields_to_drop:
            self.fields.pop(field)

class BaseViewSet(viewsets.ModelViewSet, QueryFieldsMixin):

    def batch_update(self, request, *args, **kwargs):
        data = self.before_batch_update(request)
        queryset = self.filter_queryset(self.get_queryset())

        queryset.update(**data)
        return queryset.values()

    def before_batch_update(self, request):
        return request.data

    @classmethod
    def as_view(cls, actions=None, **initkwargs):

        for func_name in actions.values():
            func = getattr(cls, func_name)
            func = json_resp(func)
            setattr(cls, func_name, func)
        return super(BaseViewSet, cls).as_view(actions, **initkwargs)

def http_json_response(data, code=status.HTTP_200_OK):
    """
    直接返回data的json格式数据
    这个接口留给GET请求用
    :param data:
    :return:
    """
    json_data = {
            "code": 0,
            "msg": "OK",
            "body": data
        }
    return HttpResponse(json.dumps(json_data, cls=DjangoJSONEncoder), content_type='application/json', status=code)


def bad_request(err, code=1):
    json_data = {
        "code": code,
        "msg": str(err),
        "body": None
    }
    return HttpResponse(json.dumps(json_data, cls=DjangoJSONEncoder), content_type='application/json', status=status.HTTP_400_BAD_REQUEST)


def compose_json_return(is_success, msg='', data=None, status=status.HTTP_200_OK):
    """
    包装了包含data的json格式数据
    附加一些is_success\msg等数据，主要是给POST请求的返回值
    :param is_success:
    :param msg:
    :param data:
    :param status:
    :return:
    """
    json_data = {}
    try:
        if is_success:
            json_data['is_success'] = True
            if data is not None:
                json_data['data'] = data
            return HttpResponse(
                json.dumps(json_data, cls=DjangoJSONEncoder), content_type='application/json', status=status)
        else:
            json_data['is_success'] = False
            if len(msg) > 0:
                json_data['msg'] = msg
            return HttpResponse(
                json.dumps(json_data, cls=DjangoJSONEncoder), content_type='application/json', status=status)
    except Exception:
        print(traceback.format_exc())
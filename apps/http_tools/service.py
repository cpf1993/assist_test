# coding=utf-8
import requests

from django.db import connections
from .models import HttpInterface



# 获取某个项目下具体的小工具并返回
def get_project_and_interface():
    res = []

    sql = "select hi.id, hi.title, hi.project_id, p.project_name " \
          "from http_interface as hi " \
          "left join project as p on hi.`project_id`=p.id"

    with connections["assist_test"].cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        data = {}
        for r in rows:
            key = (r[2],r[3])
            if key not in data:
                data[key] = []
            data[key].append(
                {"id": r[0], "name": r[1]}
            )

        for key in data:
            res.append({
                "project_id":key[0],
                "name": key[1],
                "tools": data[key]
            })

    return res


# 获取http_interface详情
def get_http_interface_info(id):
    try:
        http_interface = HttpInterface.objects.get(id=id)
    except HttpInterface.DoesNotExist:
        raise Exception(u"该接口工具不存在")

    res = dict()
    # 接口工具基本信息
    res['id'] = http_interface.id
    res['request_header_param'] = eval(http_interface.request_header_param) if http_interface.request_header_param else ""
    res['request_body_param'] = eval(http_interface.request_body_param) if http_interface.request_header_param else ""
    res['title'] = http_interface.title
    res['create_user'] = http_interface.create_user
    res['tool_note'] = http_interface.tool_note
    res['url'] = http_interface.url
    res['method'] = http_interface.method
    res['data_type'] = http_interface.data_type
    res['create_time'] = http_interface.create_time
    res['update_time'] = http_interface.update_time
    res['project'] = http_interface.project.id

    return res


# 获取id，运行http接口工具并返回
def run_http_interface(id):
    try:
        http_interface = HttpInterface.objects.get(id=id)
    except HttpInterface.DoesNotExist:
        raise Exception(u"该接口工具不存在")

    url = http_interface.url
    headers = eval(http_interface.request_header_param) if http_interface.request_header_param else ""
    data_type = http_interface.data_type
    param_data = eval(http_interface.request_body_param) if http_interface.request_header_param else ""
    method = http_interface.method

    res = run_request(url=url, method=method, headers=headers, data_type=data_type, param_data=param_data)
    return  res


def run_request(url, method, headers, data_type, param_data):
    if param_data == {}:
        param_data = None
    if headers == {}:
        headers = None

    if method == "GET":
        if data_type == "params":
            res = requests.get(url=url, headers=headers, params=param_data)
    elif method == "POST":
        if data_type == "json":
            res = requests.post(url=url, headers=headers, json=param_data)
        elif data_type == "data":
            res = requests.post(url=url, headers=headers, data=param_data)
    elif method == "PUT":
        if data_type == "json":
            res = requests.put(url=url, headers=headers, json=param_data)
        elif data_type == "data":
            res = requests.put(url=url, headers=headers, data=param_data)
    elif method == "DELETE":
        res = requests.delete(url=url, headers=headers, params=param_data)
    elif method == "PATCH":
        if data_type == "json":
            res = requests.patch(url=url, headers=headers, json=param_data)
        elif data_type == "data":
            res = requests.patch(url=url, headers=headers, data=param_data)
    result = res.json()

    return result





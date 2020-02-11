# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from apps.wms_center.host_info import PDA_WAREHOUSES
from schema import Schema, SchemaError
from apps.common.escape import schema_unicode_upper, schema_date_arrow
from apps.wms_center.consts import TEST_WAREHOUSE_MAPPING, TEST_PDA_MAPPING, header, TEST_TASK_MAPPING, CELERY_TASK
from apps.external.services import wms_api
import requests
import json
import urllib.parse as urlparse
from apps.wms_center.models import DailyCargoPlan, IdleSku


# 方法迁移
def strTodate(str):
    date = datetime.datetime.strptime(str, "%Y-%m-%d")
    return date


def dateTostr(date):
    str = date.strftime("%Y%m%d")
    return str


@login_required()
def gip_search(request):
    return render(request, "WMS/wms-gip-search.html")


def get_gip_info(request, *args, **kwargs):
    # request返回的是对象
    data = request.POST.dict()
    # 后期优化，字符串传入分割
    sku_ids = []
    sku_id = int(data["sku_id"])
    sku_ids.append(sku_id)
    resp = wms_api.storage_search(sku_ids)
    return render(request, "WMS/wms-search-result.html", {'result': resp})


# 绑定闲置库存页面
@login_required()
def bind_idleSku(request, *args, **kwargs):
    return render(request, "WMS/wms-bind-idle_sku.html")


# 查询是否有库存
def idle_sku_get(sku_id, wh_id):
    idle_sku_query_set = IdleSku.objects.using(wh_id).filter(status='IDLE_UNALLOCATED', sp_name='', sku_id=sku_id)[:1]
    result = idle_sku_query_set.values()
    return result


# 绑定闲置库存操作
@login_required()
def confirm_bind(request, *args, **kwargs):
    # request返回的是对象
    data = request.POST.dict()
    sp_name = data["sp_name"]
    sku_id = data["sku_id"]
    wh_id = data["wh_id"]
    idle_sku_query_set = idle_sku_get(sku_id, wh_id=wh_id)
    error_result = '没有可以绑定sku_id: %s 的IDLE_UNALLOCATED库存，请去WMS系统添加入库单增加库存' % sku_id
    if not idle_sku_query_set:
        return render(request, "WMS/wms-bdskuresult.html", {'result': error_result})
    idle_sku_id = idle_sku_query_set[0]['id']
    idle_sku_update = IdleSku.objects.using(wh_id).filter(sku_id=sku_id, id=idle_sku_id, ).update(sp_name=sp_name)
    return render(request, "WMS/wms-bdskuresult.html", {'result': '绑定成功'})


# WMS-仓储操作指南展示方法
@login_required()
def operateGuide(request):
    return render(request, "WMS/wms-operateGuide.html")


# 查询大货计划页面
@login_required()
def get_dailyCargoPlan(request):
    return render(request, "WMS/wms-getdailycargoplan.html")


# 获取大货计划
@login_required()
def get_dailycgPlanResult(request):
    data = request.POST.dict()
    wh_id = data["wh_id"]
    plan_query_set = DailyCargoPlan.objects.using(wh_id).all()
    plan_result = plan_query_set.values()
    return render(request, "WMS/wms-getDailyCgPlanResult.html", {'result': plan_result, 'warehouse': wh_id})


# 通过id查询大货计划
@login_required()
def getDailyCgPlanById(request):
    wh_id = request.GET.get('whid')
    plan_id = request.GET.get('id')
    plan_query_set = DailyCargoPlan.objects.using(wh_id).filter(id=plan_id)
    plan_result = plan_query_set.values()
    return render(request, "WMS/wms-editDailyCargoPlan.html",
                  {'result': plan_result, 'warehouse': wh_id, 'id': plan_id})


"""
 数据库连接更改，暂时暴力操作不判断是否更新异常
"""


# 大货计划编辑页面
def editDailyCgPlan(request):
    data = request.POST.dict()
    try:
        validate_data = Schema({
            "plan_date": schema_date_arrow
        }, ignore_extra_keys=True).validate(data)
    except SchemaError as e:
        return HttpResponse(e)
    plan_id = data["id"]
    warehouse = data["warehouse"]
    plan_date = data["plan_date"]
    quota = data["quota"]
    shipped_num = data["shipped_num"]
    update_cargo_plan = DailyCargoPlan.objects.using(warehouse).filter(id=plan_id).update(plan_date=plan_date,
                                                                                          quota=quota,
                                                                                          shipped_num=shipped_num)
    messages.success(request, '编辑成功')
    return render(request, 'WMS/wms-getdailycargoplan.html')


# pda上架工具初始界面
def operate_shelve_tool(request):
    return render(request, "WMS/wms-operateShelveTool.html")


# pda上/下架操作
def pda_operate_shelve(request):
    data = request.POST.dict()
    try:
        validate_data = Schema({
            'warehouse': schema_unicode_upper,
            'box_name': schema_unicode_upper,
            'barcode': schema_unicode_upper,
            "operate_type": schema_unicode_upper
        }, ignore_extra_keys=True).validate(data)
    except SchemaError as e:
        return HttpResponse(e)
    operate_type = data['operate_type']
    warehouse = data['warehouse']
    if warehouse not in PDA_WAREHOUSES:
        return HttpResponse("当前仓库不存在")
    del data['warehouse']
    del data['operate_type']
    data_json = json.dumps(data)
    warehouse_url = TEST_WAREHOUSE_MAPPING[warehouse]
    operate_shelve_url = TEST_PDA_MAPPING["operate_shelve"]
    operate_off_shelf = TEST_PDA_MAPPING["operate_off_shelf"]
    if operate_type == "operate_shelve":
        pda_url = urlparse.urljoin(warehouse_url, operate_shelve_url)
    else:
        pda_url = urlparse.urljoin(warehouse_url, operate_off_shelf)
    pda_shelve_resp = requests.patch(headers=header, url=pda_url, data=data_json)
    if pda_shelve_resp.status_code == 200:
        messages.success(request, '操作成功')
        return render(request, 'WMS/wms-operateShelveTool.html')
    else:
        pda_shelve_resp = json.loads(pda_shelve_resp.text)
        messages.success(request, pda_shelve_resp['message'])
        return render(request, 'WMS/wms-operateShelveTool.html')


# 定时任务工具初始页面
def time_task(request):
    return render(request, "WMS/wms-timeTaskTool.html")


# 暂时这样等待优化，有些未做强制逻辑校验
def celery_task(request):
    data = request.POST.dict()
    task_name = data['task_name']
    warehouse = data['wh_name']
    if task_name not in CELERY_TASK:
        return HttpResponse('任务不存在')
    data = {
        "task_name": task_name
    }
    json_ttn = json.dumps(data)
    warehouse_url = TEST_WAREHOUSE_MAPPING[warehouse]
    task_url = TEST_TASK_MAPPING['celery_task']
    celery_task_url = urlparse.urljoin(warehouse_url, task_url)
    task_resp = requests.post(url=celery_task_url, headers=header, data=json_ttn)
    if task_resp.status_code == 200:
        messages.success(request, '调用成功')
        return render(request, "WMS/wms-timeTaskTool.html")
    else:
        task_resp = json.loads(task_resp.text)
        messages.success(request, task_resp['message'])
        return render(request, "WMS/wms-timeTaskTool.html")

# coding=utf-8
import requests
import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from apps.external.services.po_center import GWPoAPI, GWBillAPI, LogAPI

from .models import PurchaseOrder, Bill

import re



# 获取最新生成的15条po单列表.
@login_required
def po_index(request):
    po_list = PurchaseOrder.objects.order_by("-id")[:14]
    return render(request, 'PMS/po-index.html', {'po_list': po_list})


# 网关调用po-center服务创建PO单
@login_required()
def singlepo_create(request):
    if request.method == 'POST':
        sku_id = request.POST['sku_id']
        demand = request.POST['demand']
        wh_id = request.POST['wh_id']
        user_id = request.POST['user_id']
        user_name = request.POST['user_name']
        activity_id = request.POST['activity_id']
        print(activity_id)
        if activity_id is '':
            res = GWPoAPI.create_po(sku_id, demand, wh_id, user_id, user_name)
            if res != []:
                return HttpResponseRedirect("/purchase_order/create_po/")
            elif res == []:
                return render(request, 'PMS/po-create.html', {'error': '生成PO单失败，请检查SKU是否正确!'})
        elif activity_id is not '':
            res = GWPoAPI.create_activity_po(sku_id, demand, wh_id, activity_id, user_id, user_name)
            if res != []:
                return HttpResponseRedirect("/purchase_order/create_po/")
            elif res == []:
                return render(request, 'PMS/po-create.html', {'error': '生成活动PO单失败，请检查SKU是否正确!'})

    return render(request, "PMS/po-create.html")

# 网关调用po-center服务修改PO单
@login_required()
def po_update(request):
    if request.method == 'POST':
        uuid = request.POST['uuid']
        source_type = request.POST['source_type']
        qty_system_demand = request.POST['qty_system_demand']
        qty_purchased = request.POST['qty_purchased']
        state = request.POST['state']
        cooperative_supplier = request.POST['cooperative_supplier']
        user_id = request.POST['user_id']
        user_name = request.POST['user_name']

        try:
            res = GWPoAPI.update_po(uuid, user_id, user_name, sourceType=source_type, state=state,
                                    qtySystemDemand=qty_system_demand, qtyPurchased=qty_purchased,
                                    cooperativeSupplier=cooperative_supplier)
        except Exception as e:
            return render(request, 'PMS/po-update.html', {'message': str(e)})
        if res is None:
            return render(request, 'PMS/po-update.html', {'message': u'更新成功'})
        else:
            return render(request, 'PMS/po-update.html', {'message': res})

    return render(request, "PMS/po-update.html")

# 获取最新生成的15条账单列表.
@login_required()
def bill_index(request):
    bill_list = Bill.objects.order_by("-id")[:14]
    return render(request, 'PMS/bill-index.html', {'bill_list': bill_list})

# 网关调用po-center服务创建账单
@login_required()
def bill_create(request):
    if request.method == 'POST':
        po_id_str = request.POST['po_id_list']
        po_id_list = re.split(',|，', po_id_str)
        supplier_uuid = request.POST['supplier_uuid']
        user_id = request.POST['user_id']
        user_name = request.POST['user_name']

        try:
            res = GWBillAPI.create_bill(po_id_list, supplier_uuid, user_id, user_name)
        except Exception as e:
            return render(request, 'PMS/bill-create.html', {'error': str(e)})

        if res is None:
            return render(request, 'PMS/bill-create.html', {'error': '今日该供应商已生成账单，生成新账单失败'})
        elif res is not None:
            bill_data = Bill.objects.values('id', 'uuid', 'supplier_uuid', 'supplier_name', 'create_time', 'wh_id').filter(id=res)
            return render(request, 'PMS/bill-create.html', {'bill_data': bill_data})

    return render(request, "PMS/bill-create.html")


# 网关调用po-center服务查询日志
@login_required()
def po_log(request):
    if request.method == 'POST':
        object_type = request.POST['object_type']
        object_id = request.POST['object_id']

        try:
            res = LogAPI.po_log(object_type, object_id)
        except Exception as e:
            return render(request, 'PMS/po-log.html', {'error': str(e)})
        if res is None:
            return render(request, 'PMS/po-log.html', {'error': '查询日志失败，请重试。'})
        else:
            result = res.get("logMessageInfoList")
            result_json = json.dumps(result, indent=4, ensure_ascii=False)
            return render(request, 'PMS/po-log.html', {'result_json': result_json})
    return render(request, "PMS/po-log.html")





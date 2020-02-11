# coding=utf-8
"""
po-center service
"""

from apps.external.utils.gateway import Gateway
from apps.common.exception import RPCException


class GWPoAPI:
    PO_API__CREATE_PO = ""
    PO_API__CREATE_ACTIVITY_PO = ""
    PO_API__UPDATE_PO = ""

    @classmethod
    def create_po(cls, sku_id, demand, wh_id, user_id, user_name):
        poDTO = {
            "createPOParamDTOList": [
                {
                    "skuId": int(sku_id),
                    "demand": int(demand)
                }
            ],
            "whId": int(wh_id),
            "user": {
                "id": int(user_id),
                "name": user_name
            }
        }
        data = poDTO
        res = Gateway.request(cls.PO_API__CREATE_PO, data=data)
        return res

    @classmethod
    def create_activity_po(cls, sku_id, demand, wh_id, activity_id, user_id, user_name):
        poDTO = {
            "createPOParamDTOList": [
                {
                    "skuId": int(sku_id),
                    "demand": int(demand)
                }
            ],
            "whId": int(wh_id),
            "activityId": int(activity_id),
            "user": {
                "id": int(user_id),
                "name": user_name
            }
        }
        data = poDTO
        res = Gateway.request(cls.PO_API__CREATE_ACTIVITY_PO, data=data)
        return res

    @classmethod
    def update_po(cls, uuid, user_id, user_name, **kwargs):
        poDTO = {
            "updatePurchaseOrderParamTestDTO": kwargs,
            "purchaseOrderUuid": uuid,
            "user": {
                "id": int(user_id),
                "name": user_name
            }
        }
        data = poDTO
        res = Gateway.request(cls.PO_API__UPDATE_PO, data=data)
        return res


class LogAPI:
    PO_API__PO_LOG = ""

    @classmethod
    def po_log(cls, object_type, object_id):
        logDTO = {
            "objectType": int(object_type),
            "objectId": int(object_id)
        }
        data = logDTO
        res = Gateway.request(cls.PO_API__PO_LOG, data=data)
        return res






class GWBillAPI:
    BILL_API__CREATE_BILL = ""

    @classmethod
    def create_bill(cls, po_id_list, supplier_uuid, user_id, user_name):
        billDTO = {
            "createBillParamDTO": {
                "poIdList": po_id_list,
                "supplierUuid": supplier_uuid
            },
            "user": {
                "id": user_id,
                "name": user_name
            }
        }
        data = billDTO
        try:
            bill_id = Gateway.request(cls.BILL_API__CREATE_BILL, data=data)
        except Exception as e:
            if hasattr(e, "message"):
                raise  RPCException(e.message)
            raise RPCException(str(e))
        return bill_id

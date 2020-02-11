from apps.external.utils.gateway import Gateway


class WMSApi:
    WO_API__query_storage = ""

    @classmethod
    def storage_search(cls, sku_ids: list, biz_type=3):
        storage_search_dto = {
            "query": {
                "bizType": biz_type,
                "skuIds": sku_ids
            }
        }
        search_resp = Gateway.request(cls.WO_API__query_storage, data=storage_search_dto)
        result = search_resp.get("isSuccess", False)
        model = []
        if result:
            model = search_resp["model"]
        return model


wms_api = WMSApi()

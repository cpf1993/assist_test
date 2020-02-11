from django.db import models


class DailyCargoPlan(models.Model):
    """
    大货计划
    """
    id = models.IntegerField(primary_key=True, auto_created=True, help_text='主键id')
    plan_date = models.DateField(null=False, help_text="计划日期")
    country = models.CharField(max_length=32, null=False, default='', help_text="国家")
    quota = models.CharField(max_length=255, default='{}', null=False, help_text="json_str, 目的港的每日计划量")
    shipped_num = models.CharField(max_length=255, default='{}', null=False, help_text="json_str, 目的港每日实际发送量")
    update_time = models.DateTimeField(auto_now=True, help_text="更新时间")
    create_time = models.DateTimeField(auto_now_add=True, help_text="创建时间")

    class Meta:
        app_label = "wms_center",
        db_table = "daily_cargo_plan"


class IdleSku(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, help_text='主键id')
    barcode = models.CharField(max_length=16, null=False, default='', help_text="仓库内部条形码")
    sku_id = models.IntegerField(null=False, default=0, help_text='商品id')
    status = models.CharField(max_length=32, null=False, default='IDLE_UNALLOCATED', help_text="状态")
    sku_category = models.CharField(max_length=16, null=False, default='', help_text="商品的库存类型")
    box_name = models.CharField(max_length=16, null=False, default='', help_text="分配库位的编号")
    box_id = models.IntegerField(null=False, default=0, help_text='分配库位的id')
    assignee_name = models.CharField(max_length=32, null=False, default='', help_text="负责人名字")
    assignee_id = models.IntegerField(null=False, default=0, help_text='负责人id')
    update_time = models.DateTimeField(auto_now=True, help_text="更新时间")
    create_time = models.DateTimeField(auto_now_add=True, help_text="创建时间")
    warehouse_id = models.IntegerField(null=False, default=0, help_text='[暂时没用] 仓库id')
    sp_name = models.CharField(max_length=16, null=False, default='', help_text="出库单编号")
    stock_type = models.IntegerField(null=False, default=1, help_text='库存属性')
    inventory_sts = models.IntegerField(null=False, default=1, help_text='库存质量状态')
    container_id = models.IntegerField(null=False, default=0, help_text='容器ID')

    class Meta:
        app_label = "wms_center",
        db_table = "idle_sku"

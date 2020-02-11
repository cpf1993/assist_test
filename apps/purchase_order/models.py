# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid


class SupplyOrder(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, help_text='uuid')
    platform = models.CharField(max_length=32, help_text='平台')
    external_order_id = models.CharField(db_index=True, max_length=32, help_text='第三方订单号')
    carrier_name = models.CharField(max_length=32, null=True, help_text='物流公司')
    tracking_no = models.CharField(max_length=64, null=True, help_text='物流单号')
    supplier_member_id = models.CharField(max_length=64, help_text='供应商member id')
    buyer_member_id = models.CharField(max_length=64, help_text='购买账号member id')
    pay_rmb = models.DecimalField(max_digits=12, decimal_places=2, help_text='订单实际支付金额（含运费和优惠）')
    freight_rmb = models.DecimalField(max_digits=12, decimal_places=2, help_text='运费')
    order_create_time = models.DateTimeField(null=True, help_text='订单创建时间')
    pay_time = models.DateTimeField(null=True, help_text='付款时间')
    all_delivered_time = models.DateTimeField(null=True, help_text='卖家发货时间')
    wh_id = models.PositiveSmallIntegerField(default=1, help_text='仓库id')

    create_time = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, help_text='修改时间')

    create_user_id = models.IntegerField(help_text='创建者')
    create_user_name = models.CharField(max_length=64, null=True, help_text='创建者的名字')

    class Meta:
        app_label = "purchase_order"
        db_table = "supply_order"



class ShippingTicket(models.Model):
    """
    物流单号相关的模型
    """
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, help_text='uuid')
    carrier_name = models.CharField(max_length=32, help_text='物流公司')
    carrier_id = models.CharField(max_length=32, help_text='物流id号')
    tracking_no = models.CharField(max_length=64, help_text='物流单号')

    freight_rmb = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2, help_text='运费/元')
    weight_kg = models.DecimalField(
        default=0.000, max_digits=12, decimal_places=3, help_text="重量/KG")
    pay_status = models.CharField(
        max_length=64,
        null=False, help_text='结算状态:NOT_IN_BILL(未结),IN_BILL(已结)', default="NOT_IN_BILL")

    create_time = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    # source_type:物流单信息来源. 0 系统，source_type = 1 人工
    source_type = models.PositiveSmallIntegerField(
        default=1, help_text='物流单信息来源. 0：系统, 1: 人工')
    delivery_status = models.PositiveSmallIntegerField(
        default=0, help_text='物流单揽收状态. 0: 未揽收, 1: 已揽收, 2: 揽收异常, 3: 第三方接口已签收, 4: 第三接口派送失败')
    supply_orders = models.ManyToManyField(
        SupplyOrder, related_name='shipping_tickets', help_text='相关订单')

    # 添加签收信息
    signed_date = models.DateTimeField(
        null=True, help_text='签收时间，同时这个也表示状态，有签收时间，表示已签收，没签收时间，表示未签收')
    signed_user = models.CharField(
        max_length=64, null=True, help_text='签收的用户名字')
    qty_po = models.PositiveSmallIntegerField(
        default=0, help_text="表示该物流单号对应采购批次的数量")
    task_id = models.BigIntegerField(
        default=0, db_index=True, help_text='该包裹对应任务的id')
    signed_status = models.PositiveSmallIntegerField(
        default=0, help_text='签收状态. 0: 签收, 1: 订单号不存在')
    signed_note = models.TextField(
        blank=True, null=True, help_text='签收备注')
    pay_bill = models.ForeignKey(
        "Bill", related_name='pay_ship_tickets', on_delete=models.PROTECT, blank=True, null=True, help_text='最终结算的账单[Bill]->id')

    api_collected_time = models.DateTimeField(null=True, help_text='第三方快递接口揽收时间')
    api_signed_time = models.DateTimeField(null=True, help_text='第三方快递接口签收时间')
    api_last_time = models.DateTimeField(null=True, help_text='第三方快递接口最近一条物流时间')

    @property
    def warehouse_sign_status(self):
        # 仓库pda签收状态, 0: 未签收,1:已签收,2:异常(拒收)
        if self.signed_date and self.signed_status == 0:
            return 1
        if self.signed_status == 1:
            return 2

        return 0

    class Meta:
        app_label = "purchase_order"
        db_table = "shipping_ticket"


class ShippingTicketQinMessageInfo(models.Model):
    carrier_name = models.CharField(max_length=32, help_text='物流公司', db_index=True)
    tracking_no = models.CharField(max_length=64, help_text='物流单号')
    delivery_status = models.PositiveSmallIntegerField(
        default=0, help_text='物流单揽收状态. 0: 未揽收, 1: 已揽收, 2: 揽收异常, 3: 第三方接口已签收, 4: 第三接口派送失败')
    state = models.CharField(
        max_length=32, default='', help_text='qin快递接口返回的状态')

    first_area_name = models.CharField(max_length=32, default='', help_text='第一条物流信息的位置')
    last_area_name = models.CharField(max_length=32, default='', help_text='最后一条物流信息的位置')

    message_detail = models.TextField(default='', help_text='订阅快递物流信息消息')
    message_count = models.IntegerField(help_text='快递物流信息接收次数')

    create_time = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, help_text='更新时间')

    class Meta:
        unique_together = ['tracking_no', 'carrier_name']
        app_label = "purchase_order"
        db_table = "shipping_ticket_qin_message_info"



class PurchaseOrder(models.Model):
    """
    由于认证剥离出去的原因，原来用户信息中带_user后缀的字段，仍然保持不变，在迭代后系统中表示user_id的含义
    新添加_user_name的字段，表示用户的名字
    """
    uuid = models.CharField(max_length=32, blank=True, help_text='uuid')
    short_uuid = models.CharField(
        max_length=20, blank=True, help_text='uuid后12位')

    # 采购者信息
    follow_user_id = models.IntegerField(help_text='采购负责人')
    follow_user_name = models.CharField(
        max_length=64, null=True, help_text='采购负责人的名字')

    qty_system_demand = models.PositiveIntegerField(
        default=0, help_text='系统需求采购量')
    qty_purchase_demand = models.PositiveIntegerField(
        default=0, help_text='人工需求采购量')
    qty_purchased = models.PositiveIntegerField(default=0, help_text='采购量')
    purchased_rmb = models.DecimalField(max_digits=12, decimal_places=2, help_text='实际采购金额')
    qty_received = models.PositiveIntegerField(default=0, help_text='入库量')

    qty_signed = models.PositiveIntegerField(default=0, help_text='签收数量')
    signed_time = models.DateTimeField(null=True, help_text='最近一次签收的时间')

    # 签收者信息
    signed_user_id = models.IntegerField(help_text='签收修改者的id')
    signed_user_name = models.CharField(
        max_length=64, null=True, help_text='签收修改者的名字')

    purchase_company_name = models.CharField(
        blank=True, null=True, max_length=64, help_text='供应商名')
    purchase_link = models.TextField(blank=True, null=True, help_text='供应商链接')
    purchase_link_note = models.TextField(
        blank=True, null=True, help_text='采购规格')
    purchase_price = models.FloatField(null=True, help_text='采购价格')
    wh_id = models.PositiveSmallIntegerField(
        default=0, help_text='仓库id')

    # 创建信息
    create_time = models.DateTimeField(auto_now_add=True, help_text='采购单生成时间')
    create_user_id = models.IntegerField(help_text='采购单创建者')
    create_user_name = models.CharField(
        max_length=64, null=True, help_text='创建者的名字')

    # 购买信息
    purchase_time = models.DateTimeField(null=True, help_text='购买时间')
    purchase_user_id = models.IntegerField(help_text='购买者')
    purchase_user_name = models.CharField(
        max_length=64, null=True, help_text='购买者的名字')

    # 更新信息
    update_time = models.DateTimeField(
        null=True, auto_now=True, help_text='修改时间')
    update_user_id = models.IntegerField(help_text='采购单修改者')
    update_user_name = models.CharField(
        max_length=64, null=True, help_text='修改者的名字')

    # 完成信息
    complete_time = models.DateTimeField(null=True, help_text='采购单完成时间')
    complete_user_id = models.IntegerField(help_text='采购单完成者')
    complete_user_name = models.CharField(
        max_length=64, null=True, help_text='采购单完成者的名字')

    source_type = models.PositiveSmallIntegerField(
        default=1, help_text='来源种类.0: 系统, 1: 人工, 2: 补单,')
    # normal = 0, abnormal = 1
    difficult_order = models.BooleanField(
        default=0, help_text='是否是疑难单. 0:否, 1:是,')

    # 疑难信息
    difficult_order_follower_id = models.IntegerField(help_text='疑难单负责人')
    difficult_order_follower_name = models.CharField(
        max_length=64, null=True, help_text='疑难单负责人的名字')

    has_backorder = models.PositiveSmallIntegerField(
        default=0, help_text='是否有补单. 0:没有补单. 1:有补单')
    has_bought = models.PositiveIntegerField(
        default=0, help_text='是否已买，默认为0，表示没有买')

    source_purchase_order = models.ForeignKey(
        'self', null=True, on_delete=models.PROTECT, help_text='源单')

    top_source_purchase_order = models.ForeignKey(
        'self', null=True, on_delete=models.PROTECT, help_text='源单',
        related_name="+")
    source_purchase_order_uuid = models.CharField(
        max_length=32, null=True, help_text='来源uuid')
    top_source_purchase_order_uuid = models.CharField(
        max_length=32, null=True, help_text='首次来源uuid')

    state = models.SmallIntegerField(
        default=0,
        help_text='采购单状态. -1:未下单 0:未采购, 1:已采购, 2:已发货, 3:部分入库, 4:全部入库, 5:部分缺货, 6:全部缺货, 7:取消, 8:已下单')
    sku_sale_price = models.FloatField(null=True, help_text='销售单价.从odoo同步过来的.')
    shipping_tickets = models.ManyToManyField(
        ShippingTicket, related_name='purchase_orders',
        blank=True, help_text='物流运单')
    supply_order = models.ForeignKey(
        SupplyOrder, on_delete=models.SET_NULL,
        null=True, related_name='purchase_orders', help_text='订单')
    # 物流状态 0: 无运单， 1：全部是未揽收单， 2：全部是揽收单，3：部分揽收且无未知单，
    # 4：部分揽收且有未知单， 5：只有未知单和未揽收单， 6：全部是未知单, 7: 已签收
    logistics_status = models.PositiveSmallIntegerField(
        default=0, help_text='物流状态')

    receive_user_id = models.IntegerField(help_text='对版负责人id')
    receive_user_name = models.CharField(
        max_length=64, null=True, help_text='对版负责人名字')
    is_exception = models.BooleanField(
        default=0, help_text='是否标记异常. 0:否, 1:是,')
    is_cooperative_supplier = models.BooleanField(
        default=0, help_text='是否来自于合作供应商. 0:否, 1:是,')
    prev_state = models.SmallIntegerField(default=0, help_text="前一种状态")
    purchase_sku_barcode = models.CharField(
        max_length=64, null=True, help_text='条形码')
    #receive_time = models.DateTimeField(null=True, help_text='收货时间，即第一次更新入库数量时间')
    supplier_uuid = models.CharField(
        max_length=64, null=True, help_text='供应商uuid')
    sku_link_rel_id = models.IntegerField(help_text='sku_link_rel -> id')
    quality_type = models.CharField(
        max_length=32, null=False, default="NORMAL", help_text='质检类型：SCORE:打分，NORMAL：普通')
    quality_score = models.FloatField(
        default=0, help_text="品质打分")

    supplier_is_disposable = models.BooleanField(
        default=0, help_text='该po单的供应商是否是一次性供应商. 0:  不是, 1: 是')
    purchased_follow_user_name = models.CharField(
        max_length=64, default='', help_text='跟单负责人的名字')
    purchased_follow_user_id = models.IntegerField(help_text='跟单负责人', default=0)

    sku_id = models.BigIntegerField(
        db_index=True, default=0, null=False, help_text='sku id')
    is_stock = models.BooleanField(
        default=0, help_text='是否备货属性. 0:否, 1:是')
    delay_bill = models.BooleanField(
        default=0, help_text='是否需要延迟结算. 0:否, 1:是')
    activity_id = models.IntegerField(
        default=0, help_text='活动id')

    @property
    def quality_inspection_method(self):
        if self.state in [0, 8]:
            return None

        if hasattr(self, 'purchase_order_quality_inspection'):
            return self.purchase_order_quality_inspection.quality_inspection_method
        else:
            return 'full_inspection'

    @property
    def qty_quality_inspection(self):
        if self.state in [0, 8]:
            return None

        if hasattr(self, 'purchase_order_quality_inspection'):
            return self.purchase_order_quality_inspection.qty_quality_inspection
        else:
            return self.qty_purchased

    class Meta:
        app_label = "purchase_order"
        db_table = "purchase_order"

    def create(self, *args, **kwargs):
        self.short_uuid = self.uuid[-12:]
        return super(PurchaseOrder, self).create(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.short_uuid = self.uuid[-12:]
        return super(PurchaseOrder, self).save(*args, **kwargs)


class PurchaseOrderExt(models.Model):
    purchase_order = models.OneToOneField(
        PurchaseOrder, on_delete=models.CASCADE,
        related_name='purchase_order_ext', help_text='po->id')

    sku_no = models.CharField(max_length=16, help_text='sku号')
    item_no = models.CharField(max_length=32, help_text='货号')
    sku_attribute = models.TextField(help_text='sku属性')
    category_id_top = models.BigIntegerField(help_text='实际商品类目id 一级')
    product_source_type = models.IntegerField(
        default=-1, help_text='商品中心上货来源 -1空 1爬虫自动上货 2爬虫人工上货 3供应商上货 4淘宝联盟 5供应商直发上货')

    class Meta:
        app_label = "purchase_order"
        db_table = "purchase_order_ext"


class PurchaseOrderQualityInspection(models.Model):
    purchase_order = models.OneToOneField(
        PurchaseOrder, on_delete=models.CASCADE,
        related_name='purchase_order_quality_inspection', help_text='po->id')

    quality_inspection_method = models.CharField(
        max_length=32, null=False, default='exempted_from_inspection',
        help_text='免检: exempted_from_inspection, 抽检: sampling_inspection')

    qty_quality_inspection = models.PositiveIntegerField(default=0, help_text='应检数量')

    purchase_company_name = models.CharField(
        null=False, max_length=64, help_text='供应商名称')

    create_time = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, help_text='更新时间')

    class Meta:
        app_label = "purchase_order"
        db_table = "purchase_order_quality_inspection"


class PurchaseOrderNotes(models.Model):
    """
    field名字的约定：
    1、如果是采购相关的note，要以purchase开头，否则都是默认入库相关的note
    2、每个note，都要有help_text
    """
    purchase_order = models.OneToOneField(
        PurchaseOrder, on_delete=models.CASCADE,
        related_name='purchase_order_notes', help_text='采购单')
    purchase_note = models.TextField(blank=True, help_text='购买备注')
    entry_note = models.TextField(blank=True, help_text='质检备注')
    receive_note = models.TextField(blank=True, null=True, help_text='对版备注')
    receive_exception_note = models.CharField(
        max_length=256, null=True, help_text='对版异常备注,逗号分割,冒号后面存数量')
    purchase_exception_note = models.TextField(blank=True, help_text='购买异常备注')
    entry_exception_note = models.TextField(blank=True, help_text='入库异常备注')
    sku_difficult_note = models.TextField(blank=True, help_text='sku对应供应商异常备注')
    supplier_note = models.TextField(blank=True, help_text='对外供应商备注')
    supplier_exception_note = models.TextField(
        blank=True, help_text='对外供应商异常备注')
    follow_purchase_order_note = models.CharField(
        max_length=128, null=True, help_text='跟单备注')
    quality_note = models.TextField(blank=True, help_text='品质扣分备注')
    third_order_icon = models.SmallIntegerField(
        help_text="第三方订单备注图标颜色:0-灰色,1-红色,2-蓝色,3-绿色,4-黄色", default=0)
    third_order_note = models.CharField(
        max_length=128, null=True, help_text='第三方订单备注', default='')

    class Meta:
        app_label = "purchase_order"
        db_table = "purchase_order_notes"


class PurchaseOrderMRP(models.Model):
    '''MRP
    '''
    sku_id = models.BigIntegerField(
        db_index=True, default=0, null=False, help_text='sku id')
    safe_qty = models.IntegerField(default=1, null=False, help_text="安全库存数量")
    min_purchase_qty = models.IntegerField(
        default=1, null=False, help_text="最小采购数量")
    # 创建信息
    create_time = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, help_text='更新时间')
    wh_id = models.PositiveSmallIntegerField(default=1, help_text='仓库id')

    # 新增版本号信息
    version = models.CharField(max_length=32, null=True, help_text="版本号")

    class Meta:
        app_label = "purchase_order"
        db_table = "purchase_order_mrp"



class Bill(models.Model):
    '''账单
    '''
    uuid = models.CharField(max_length=64, default='', help_text="账单号")
    supplier_uuid = models.CharField(
        max_length=64, null=False, help_text='供应商uuid')
    supplier_name = models.CharField(
        max_length=256, default='', help_text='供应商名')
    qty = models.PositiveIntegerField(null=False, help_text='采购单数量', default=0)
    qty_received = models.PositiveIntegerField(
        null=False, help_text='入库数量', default=0)

    purchase_rmb = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2, help_text='商品采购总金额(未打折)')
    discount = models.DecimalField(
        default=1.00, max_digits=5, decimal_places=4, help_text='折扣率')
    discount_rmb = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2, help_text='折扣后商品价格')

    freight_rmb = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2, help_text='运费金额')
    total_rmb = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2, help_text='账单总金额')

    agree_pay_time = models.DateTimeField(null=False, help_text='约定付款时间')

    pr_status = models.CharField(
        max_length=64,
        null=False, help_text='请款状态:INIT(未请款),APPLIED(已请款)', default="INIT")

    supplier_note = models.CharField(
        max_length=256, null=True, help_text='供应商备注')
    wh_id = models.PositiveSmallIntegerField(default=1, help_text='仓库id')

    create_time = models.DateTimeField(default=timezone.now, help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, help_text='更新时间')

    class Meta:
        app_label = "purchase_order"
        db_table = "bill"


class BillPurchaseOrder(models.Model):
    bill = models.ForeignKey(
        Bill, related_name='purchase_bills', help_text='[bill]->id', on_delete=models.PROTECT)
    po = models.ForeignKey(
        PurchaseOrder, related_name='purchase_bills', help_text='[purchase_order]->id', on_delete=models.PROTECT)

    qty = models.PositiveIntegerField(
        null=False, help_text='采购入库数量', default=0)
    unit_rmb = models.DecimalField(
        null=False, max_digits=12, decimal_places=2, help_text='单价', default=0.00)
    total_rmb = models.DecimalField(
        null=False, max_digits=12, decimal_places=2, help_text='总价', default=0.00)
    follow_user_name = models.CharField(max_length=32, help_text='采购负责人')

    create_time = models.DateTimeField(auto_now_add=True, help_text='创建时间')

    class Meta:
        app_label = "purchase_order"
        db_table = "bill_purchase_order"

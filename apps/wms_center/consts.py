# 分仓
WAREHOUSE_YH = ''
WAREHOUSE_XS = ''
WAREHOUSE_HN = ''
WAREHOUSE_DG = ''
WAREHOUSE_HZ2 = ''
WAREHOUSE_DG2 = ''
# 备货仓
WAREHOUSE_BH = ''
WAREHOUSE_BH2 = ''
# 印度
WAREHOUSE_INDIA = ''
WAREHOUSE_INDIA2 = ''
WAREHOUSE_INDIA3 = ''
WAREHOUSE_INDIA4 = ''
WAREHOUSE_INDIA5 = ''

# 先暂时这样写，后期看怎么拆分比较好
TEST_WAREHOUSE_MAPPING = {
    WAREHOUSE_DG2: "",
    WAREHOUSE_HZ2: "",
    WAREHOUSE_INDIA: "",
    WAREHOUSE_INDIA2: "",
    WAREHOUSE_INDIA3: "",
}
# pda上下架url
TEST_PDA_MAPPING = {
    "operate_shelve": "",
    "operate_off_shelf": ""
}
# 定时任务url
TEST_TASK_MAPPING = {
    "celery_task": "",
}
# 定时任务集合
CELERY_TASK = ["", ""]

# 用户操作信息
cookie = ''
header = {
    "Authorization": cookie,
    "Content-Type": "application/json"

}

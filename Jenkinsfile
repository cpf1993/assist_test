import groovy.transform.Field

// 接收报警的用户的企业微信ID(即工号)列表，用英文逗号分隔
@Field
List<Integer> Infoee = [207,486,438]

// 开发语言
@Field
String Language = 'erp_python'

// App 名称
@Field
String AppName = 'assist_test'

// 运行命令
@Field
String AppExec = 'bash ./deploy/deploy.sh'

// 健康检查
@Field
String HealthUrl = 'http://localhost/auth/check_health/'

// 开发机器, 地址类型：['aws:loc:u:ip:port',]
@Field
List<String> Devs = []

// 测试机器, 地址类型：['aws:loc:u:ip:port',]
@Field
List<String> Tests = [
             ''
]

// 预发机器, 地址类型：['aws:loc:u:ip:port',]
@Field
List<String> Pres = []

// 生产机器, 地址类型：['aws:loc:u:ip:port',]
@Field
List<String> Prods = []

// 逻辑入口。永远不要修改之后的内容。
ErpCI(this)

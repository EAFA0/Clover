import os

# 是否开启debug模式
DEBUG = True

AppID = ""
AppSecret = ""
AccessToken = ""

# 读取数据库环境变量
username = os.environ.get("MYSQL_USERNAME", 'root')
password = os.environ.get("MYSQL_PASSWORD", 'pwd')
db_address = os.environ.get("MYSQL_ADDRESS", '127.0.0.1:3306')

template_id = {
    "纪念日推送": "qov0zOd4gI6v-WRoMiujnlR7DI116wLFK0G_A4qalAE"
}

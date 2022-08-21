import os

# 是否开启debug模式
DEBUG = True

AppID = "wx537158349763b0c1"
AppSecret = "664173c49f909ea04562b2d22414e2d2"

# 读取数据库环境变量
username = os.environ.get("MYSQL_USERNAME", 'root')
password = os.environ.get("MYSQL_PASSWORD", 'pwd')
db_address = os.environ.get("MYSQL_ADDRESS", '127.0.0.1:3306')

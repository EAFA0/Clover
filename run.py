import sys
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

# 启动Flask Web服务
if __name__ == '__main__':
    app.run(host=sys.argv[1], port=sys.argv[2])

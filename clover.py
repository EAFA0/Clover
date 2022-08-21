import json
import config
from requests import get
from flask import Flask
from flask import request

app = Flask(__name__)
app.config.from_object('config')


@app.route("/ping")
def ping():
    return "ok"


@app.route("/openid", methods=["GET"])
def openid():
    if val := openid(request):
        return {"openid": val}
    else:
        return {"msg": "failed"}


def openid(req: request) -> str:
    '''
    获取用户的 openid
    '''
    # 云托管服务请求头自带 openid
    if "x-wx-openid" in req.headers:
        return req.headers["x-wx-openid"]

    # 非托管服务需要在请求中带上 js_code 字段
    js_code = request.args.get("js_code", "")
    if not js_code:
        raise Exception("empty js_code")

    url = "https://api.weixin.qq.com/sns/jscode2session"
    data = {
        "appid": config.AppID,
        "secret": config.AppSecret,
        "js_code": js_code,
        "grant_type": "authorization_code",
    }
    if not (resp := get(url, params=data)):
        raise Exception("request failed")

    if resp.status_code == 200 and resp.text:
        body = json.loads(resp.text)
        if "openid" not in body:
            raise Exception("empty openid response")
        return body["openid"]

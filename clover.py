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
    if code := request.args.get("code", ""):
        url = "https://api.weixin.qq.com/sns/jscode2session"
        data = {
            "appid": config.AppID,
            "secret": config.AppSecret,
            "js_code": code,
            "grant_type": "authorization_code",
        }
        if (resp := get(url, params=data)) and resp.status_code == 200 and resp.text:
            if (body := json.loads(resp.text)) and "openid" in body:
                return {"openid": body["openid"]}
            else:
                return body["errmsg"] if "errmsg" in body else "error"

    return {
        "msg": "failed"
    }, 502

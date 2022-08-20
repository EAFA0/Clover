from typing import Mapping
import config
from requests import get, post
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

    if resp.status_code == 200 and (body := resp.json()):
        if "openid" not in body:
            raise Exception("empty openid response")
        return body["openid"]


def access_token() -> str:
    '''
    获取各接口所需的 access_token 字段, doc:

    https://developers.weixin.qq.com/doc/offiaccount/WeChat_Invoice/Nontax_Bill/API_list.html
    '''
    if ac := config.AccessToken:
        return ac

    url = "https://api.weixin.qq.com/cgi-bin/token"
    data = {
        "grant_type": "client_credential",
        "appid": config.AppID,
        "secret": config.AppSecret,
    }

    # todo access_token 有过期时间的限制
    # 需要在内存中实现缓存逻辑

    resp = get(url, data).json()
    if "access_token" not in resp:
        msg = "request access_token failed: "
        raise Exception(msg, resp)

    config.AccessToken = ["access_token"]
    return config.AccessToken


def template_message(user_id: str, template_name: str, data: Mapping):
    '''
    往指定用户发送模板信息, doc:

    https://mp.weixin.qq.com/debug/cgi-bin/readtmpl?t=tmplmsg/faq_tmpl
    '''
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send"
    params = {"access_token": access_token()}
    data = {
        "template_id": template_id(template_name),
        # todo 默认链接到微信下载页面, 后续修改
        "touser": user_id,
        "data": data
    }

    # 检查 data 里的必须参数是否存在
    for k, v in data.items():
        if "value" not in v:
            raise Exception(f"the value field is miss, data: {k}")

    resp = post(url, data, params=params)

    # 请求失败时, 抛出错误信息
    if errmsg := resp.json()["errmsg"]:
        raise Exception(errmsg)


def template_id(template_name: str) -> str:
    '''
    根据模板名称, 获取到对应的模板 id
    '''
    try:
        config.template_id[template_name]
    except KeyError:
        raise Exception(f"invalid template name: {template_name}")

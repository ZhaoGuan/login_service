import datetime
from urllib.parse import quote

import jwt
import msal
from jinja2 import Environment, PackageLoader, FileSystemLoader
from sanic import Blueprint, Request
from sanic.response import redirect, html
import json

import settings
from common.sanic_template import JinJaTemplate
from config import oauth_config as app_config

base_bp = Blueprint('base')


@base_bp.route('/')
async def index(request: Request):
    return redirect('/index')


@base_bp.route('/index')
async def index(request: Request):
    session = request.ctx.session
    if redirect_url := session.get('redirect'):
        return redirect(redirect_url)
    else:
        userData = session.get("user", {})
        template = JinJaTemplate().template_render_async
        response = await template('index.html')
        response.cookies['token'] = session.get('token')
        JINJA_ENV = Environment(loader=FileSystemLoader(searchpath=settings.TEMPLATES))
        JINJA_ENV.variable_start_string = '{['  # 修改块开始符号
        JINJA_ENV.variable_end_string = ']}'
        template = JINJA_ENV.get_template('index.html')
        return html(template.render(userData=json.dumps(userData)))


@base_bp.route('/login')
async def root(request: Request):
    session = request.ctx.session
    redirect_url = request.args.get('redirect')
    print("SERVICE SESSION:", session)
    if session.get("token", None):
        if redirect_url:
            return redirect('redirect_url')
        else:
            return redirect('/index')
    session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE)
    session['redirect'] = redirect_url
    userData = session.get("user", {})
    JINJA_ENV = Environment(loader=FileSystemLoader(searchpath=settings.TEMPLATES))
    JINJA_ENV.variable_start_string = '{['  # 修改块开始符号
    JINJA_ENV.variable_end_string = ']}'
    template = JINJA_ENV.get_template('login.html')
    iframeFlag = 'true' if redirect_url else 'false'
    return html(template.render(auth_url=session["flow"]["auth_uri"].replace('/v2.0', ''),
                                iframeFlag=iframeFlag, userData=json.dumps(userData)))


@base_bp.route('/oauth')
async def get_token(request: Request):
    session = request.ctx.session
    redirect_url = session.get('redirect')
    print("重定向地址,{}".format(redirect_url))
    print(request.args)
    try:
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
            session.get("flow", {}), request.args)
        user_info = result.get("id_token_claims")
        print(user_info)
        name = user_info.get("name")
        email = user_info.get("preferred_username")
        token = result.get("access_token")
        refresh_token = result.get("refresh_token")
        print("EXP", user_info.get("exp"))
        user = {"email": email, "name": name}
    except Exception as e:
        print("出现错误:{},重定向到登录!".format(e))
        return redirect('/login')
    # 声明所使用的算法
    jwt_headers = {'alg': "HS256"}
    session['token'] = jwt.encode(
        user,
        settings.SECRET,
        algorithm="HS256",  # 指明签名算法方式, 默认也是HS256
        headers=jwt_headers  # json web token 数据结构包含两部分, payload(有效载体), headers(标头)
    )
    # 写入用户信息到session
    session["user"] = user
    return redirect('/index')


@base_bp.route("/logout")
def logout(request: Request):
    session = request.ctx.session
    redirect_url = request.args.get('redirect')
    session.clear()
    if redirect_url:
        return redirect(
            app_config.AUTHORITY + "/oauth2/v2.0/logout" +
            "?post_logout_redirect_uri=" + quote(redirect_url))
    else:
        return redirect(
            app_config.AUTHORITY + "/oauth2/v2.0/logout" +
            "?post_logout_redirect_uri=" + quote(settings.FULL_REDIRECT_PATH))


def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)


def _load_cache():
    cache = msal.SerializableTokenCache()
    return cache


def _build_auth_code_flow(authority=None, scopes=None):
    return _build_msal_app(authority=authority).initiate_auth_code_flow(
        scopes or [],
        redirect_uri=settings.FULL_REDIRECT_PATH)

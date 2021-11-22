import datetime
from urllib.parse import quote

import jwt
import msal as msal
from sanic import Blueprint, Request
from sanic.response import json, text, redirect, html
from sqlalchemy import update

import settings
from app.common.response_body import JsonResponse
from app.common.sanic_template import JinJaTemplate
from app.config import oauth_config as app_config
from app.db.mysql.Users import UserTable
from app.db.service.user_service import UserSql

base_bp = Blueprint('base')


@base_bp.route('/index')
async def index(request: Request):
    template = JinJaTemplate().template_render_async
    response = await template('index.html')
    response.cookies['token'] = request.ctx.session.get('token')
    return response


@base_bp.route('/login')
async def root(request: Request):
    session = request.ctx.session
    session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE)
    template = JinJaTemplate().template_render_async
    return await template('login.html', auth_url=session["flow"]["auth_uri"])


@base_bp.route('/oauth')
async def get_token(request: Request):
    session = request.ctx.session
    db_session = request.ctx.db_session
    try:
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
            session.get("flow", {}), request.args)
        user_info = result.get("id_token_claims")
        session["user"] = user_info
        user_sql = UserSql(db_session)
        name = user_info.get("name")
        token = result.get("access_token")
        refresh_token = result.get("refresh_token")
        last_login = datetime.datetime.now()
        exp = datetime.datetime.fromtimestamp(user_info.get("exp")) if user_info.get("exp") else None
        if user := await user_sql.get_by_email(user_info.get("preferred_username")):
            update_cation = update(user_sql.model).where(
                user_sql.model.id == user.id).values({"name": name, "token": token, "refresh_token": refresh_token,
                                                      "last_login": last_login, "exp": exp})
            await user_sql.update(update_cation)
        else:
            user = UserTable()
            user.email = user_info.get("preferred_username")
            user.name = name
            user.token = token
            user.refresh_token = refresh_token
            user.last_login = last_login
            user.exp = exp
            await user_sql.add(user)
    except Exception as e:
        print(e)
        return redirect('login')
    try:
        jwt_headers = {
            'alg': "HS256",  # 声明所使用的算法
        }
        session['token'] = jwt.encode(
            user.to_dict(),
            settings.SECRET, algorithm="HS256",  # 指明签名算法方式, 默认也是HS256
            headers=jwt_headers  # json web token 数据结构包含两部分, payload(有效载体), headers(标头)
        )
        print(session['token'])
        return redirect('/index')
    except Exception as e:
        print(e)
        return redirect('/login')


@base_bp.route("/logout")
def logout(request: Request):
    session = request.ctx.session
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
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
        redirect_uri="http://localhost:8000/oauth")

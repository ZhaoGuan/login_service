import os
from contextvars import ContextVar

from sanic import Sanic
from sanic.response import redirect
from sanic_cors import CORS, cross_origin
from sanic_session import Session, InMemorySessionInterface

import settings
from .controller import app_routes
from .controller.user import user_app
from .db.mysql.db import async_db
import jwt

from .db.service.user_service import UserSql

app = Sanic(__name__)
app.config.SANIC_JWT_ACCESS_TOKEN_NAME = 'jwt'

_base_model_db_session_ctx = ContextVar("db_session")

Session(app, interface=InMemorySessionInterface())
CORS(app)


@app.middleware("request")
async def inject_session(request):
    async with async_db.engine.connect():
        request.ctx.db_session = async_db()
        request.ctx.db_session_ctx_token = _base_model_db_session_ctx.set(request.ctx.db_session)


@app.middleware("response")
async def close_session(request, response):
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_db_session_ctx.reset(request.ctx.db_session_ctx_token)
        await request.ctx.db_session.close()


@app.middleware('request')
async def run_before_handler(request):
    db_session = request.ctx.db_session
    session = request.ctx.session
    user_sql = UserSql(db_session)
    if request.path not in ['/login', '/oauth']:

        if request.token or session.get("token"):
            token = request.token if request.token else session.get("token")
            print(token)
            try:
                data = jwt.decode(token, settings.SECRET, algorithms=['HS256'])
            except Exception as e:
                print(e)
                return redirect('/login')
            request.ctx.user = await user_sql.get_by_uuid(data.get("user_id"))
        else:
            return redirect('/login')


app.blueprint(app_routes)
app.blueprint(user_app)

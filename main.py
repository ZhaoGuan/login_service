from contextvars import ContextVar

import jwt
from sanic import Sanic
from sanic.response import redirect
from sanic_cors import CORS
from sanic_session import Session, InMemorySessionInterface

import settings
from controller import app_routes
# from databases.mysql.db import async_db

app = Sanic(__name__)
app.static('/static', str(settings.BASE_DIR) + '/static')
app.config.SANIC_JWT_ACCESS_TOKEN_NAME = 'jwt'

_base_model_db_session_ctx = ContextVar("db_session")

Session(app, interface=InMemorySessionInterface())
CORS(app)


# @app.middleware("request")
# async def inject_session(request):
#     async with async_db.engine.connect():
#         request.ctx.db_session = async_db()
#         request.ctx.db_session_ctx_token = _base_model_db_session_ctx.set(request.ctx.db_session)
#
#
# @app.middleware("response")
# async def close_session(request, response):
#     if hasattr(request.ctx, "session_ctx_token"):
#         _base_model_db_session_ctx.reset(request.ctx.db_session_ctx_token)
#         await request.ctx.db_session.close()


# 强制登录
@app.middleware('request')
async def run_before_handler(request):
    session = request.ctx.session
    if request.path not in ['/', '/login', '/oauth'] and not session.get("token") and "/static/" not in request.path:
        return redirect('/login')


app.blueprint(app_routes)

if __name__ == '__main__':
    app.run('0.0.0.0', 8001, auto_reload=True)

from sanic import Blueprint, Request
from sanic.response import json

user_app = Blueprint('user', url_prefix='/user')


@user_app.get('info')
async def get_self_info(request: Request):
    print(request.ctx.user)
    return json({
        "code": 200,
        "message": "success",
        "data":{}
    })


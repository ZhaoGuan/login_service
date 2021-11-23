#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from sanic.response import json, text, html


class JsonResponse:
    def __init__(self):
        self.message = None
        self.data = None
        self.code = 200

    def success(self, data):
        self.data = data
        self.message = "Ok"
        return json({
            "code": 200,
            "data": self.data,
            "message": self.message
        })

    def error(self, data, message="Error"):
        self.data = data
        self.message = message
        return json({
            "code": 500,
            "data": self.data,
            "message": self.message
        })

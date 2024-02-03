# -*- coding: utf-8 -*-

from django.http import HttpResponse
from WikiModel.models import Page
import json


def createRsp(code, content):
    """创建返回响应"""
    return {
        "code": code,
        "content": content
    }
    pass


# 数据库操作
def testdb(request):
    test1 = Page(page_id=12)
    test1.save()
    data = {
        "user": 1
    }
    return HttpResponse(json.dumps(createRsp(200, data)))
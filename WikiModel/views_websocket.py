from django.shortcuts import render

import asyncio
import numpy as np
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import threading
from threading import Lock

from WikiModel.models import PageStatus
from WikiModel.wikisite import bot_status, bot_wiki


def savePageStatus(item):
    """保存页面状态至数据库"""
    instance = PageStatus.objects.filter(id=item['id']).first()
    if instance is None:
        instance = PageStatus(
            id=item['id'],
            title=item['title'],
            ns=item['ns'],
            target=item['target'],
            outdated=item['outdated'],
            noneTargetLangPage=item['noneTargetLangPage'],
            onewayLangLink=item['onewayLangLink'],
            multiBackLangLinks=item['multiBackLangLinks'],
        )
    else:
        instance.title = item['title']
        instance.ns = item['ns']
        instance.target = item['target']
        instance.outdated = item['outdated']
        instance.noneTargetLangPage = item['noneTargetLangPage']
        instance.onewayLangLink = item['onewayLangLink']
        instance.multiBackLangLinks = item['multiBackLangLinks']
    instance.save()


def makeResponseJson(code, data=None, length=-1, msg=""):
    return {
        "code": code,
        "data": data,
        "length": length,
        "msg": msg
    }


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def run_async_task(task):
    new_loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_loop, args=(new_loop,))
    t.start()
    asyncio.run_coroutine_threadsafe(task, new_loop)


# Create your views here.
class PageStatusConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock = Lock()
        self.should_receive = True

    async def getPageStatus_callback(self, list_ps):
        for ps in list_ps:
            savePageStatus(ps)
        response_json = makeResponseJson(200, list_ps, len(list_ps))
        await self.send(json.dumps(response_json))

    async def pull_pages(self, lang):
        print("do pull_pages_status")
        all_pages = bot_wiki.getAllPages()
        splits = np.array_split(all_pages, 10)
        result = []
        for i, split in enumerate(splits):
            print(f"Page inter-lang checked: {i*10}/{len(all_pages)}")
            list_ps = bot_status.get_pages_status(split, lang)
            result.extend(list_ps)
            await self.getPageStatus_callback(list_ps)
        response_json = makeResponseJson(200, result, len(result))
        await self.send(json.dumps(response_json))
        self.should_receive = True

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        """
        接收消息
        :param text_data: 客户端发送的消息
        :return:
        """
        request_data = json.loads(text_data)
        lang = request_data.get('lang', None)
        with self.lock:
            if self.should_receive:
                print("start receive")
                if lang is not None:
                    self.should_receive = False
                    run_async_task(self.pull_pages(lang))
                else:
                    await self.send(json.dumps(makeResponseJson(400, msg="缺少参数: lang")))
            else:
                await self.send(json.dumps(makeResponseJson(500, msg="命令执行中，拒绝重复执行")))

from django.shortcuts import render
import asyncio
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
import threading
from threading import Lock

from WikiModel.models import PageStatus
from WikiModel.wikisite import bot_status, bot_wiki
from utils.responseUtils import makeResponseJson


@sync_to_async
def savePageStatus(item):
    """保存页面状态至数据库"""
    instance = sync_to_async(PageStatus.objects.filter(id=item['id']).first())
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

    def getPageStatus_callback(self, list_ps):
        for ps in list_ps:
            savePageStatus(ps)
        response_json = makeResponseJson(200, list_ps, len(list_ps))
        self.send(json.dumps(response_json))

    async def sendResponse(self, response_json):
        """发送响应"""
        await self.send(json.dumps(response_json))
        pass

    async def pull_pages(self, lang):
        print("do pull_pages_status")
        all_pages = bot_wiki.getAllPages()
        result = []
        for i in range(0, len(all_pages), 10):
            print(f"Page inter-lang checked: {i}/{len(all_pages)}")
            list_ps = bot_status.get_pages_status(all_pages[i:i + 10], lang)
            result.extend(list_ps)
            for ps in list_ps:
                savePageStatus(ps)
            response_json = makeResponseJson(100, list_ps, len(list_ps))
            await self.sendResponse(response_json)
        response_json = makeResponseJson(200, result, len(result))
        await self.sendResponse(response_json)
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
                    await self.send(json.dumps(makeResponseJson(100, msg="仍有后续数据")))
                else:
                    await self.send(json.dumps(makeResponseJson(403, msg="缺少参数: lang")))
            else:
                await self.send(json.dumps(makeResponseJson(423, msg="命令执行中，拒绝重复执行")))

from django.shortcuts import render
import json
from django.http.response import JsonResponse
from django.db.models import Max

from WikiModel.models import Page, PageRevision, Contributor, PageDoc, PageStatus
from WikiModel.serializers import ContributorSerializer
from rest_framework.decorators import api_view

import WikiModel.wikisite.bot_format as bot_format
import WikiModel.wikisite.bot_status as bot_status
from WikiModel.wikisite import bot_wiki


@api_view(['GET', 'POST', 'DELETE'])
def page_list(request):
    """从数据库获取页面列表"""
    if request.method == 'GET':
        pages = Page.objects.all()

        # 根据ns查询页面列表
        ns = request.query_params.get('ns', None)
        if ns is not None:
            pages = Page.objects.filter(ns=ns)
        pageid = request.query_params.get('pageid', None)
        if pageid is not None:
            pages = Page.objects.filter(id=pageid)
        pages = pages.all().annotate(latest_timestamp=Max('pagerevision__timestamp'))
        table = []
        for page in pages:
            latest_revision = page.pagerevision_set.get(timestamp=page.latest_timestamp)
            print(latest_revision.contributor)
            contributor = latest_revision.contributor
            row = {
                "id": page.id,
                "title": page.title,
                "ns": page.ns,
                "redirect_title": page.redirect_title,
                "latest_timestamp": page.latest_timestamp,
                "contributorId": contributor.id,
                "contributorName": contributor.user_name,
                "contributorIP": contributor.user_ip,
                "revisionId": latest_revision.id,
                "comment": latest_revision.comment
            }
            table.append(row)

        return JsonResponse(table, safe=False)
        # 'safe=False' for objects serialization


@api_view(['GET', 'POST', 'DELETE'])
def page_status(request):
    """从数据库获取页面状态"""
    if request.method == 'GET':
        target_lang = request.query_params.get('lang', None)
        if target_lang is not None:
            result = bot_status.get_page(target_lang)
            # 尝试保存至本地数据库
            for item in result:
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
            return JsonResponse(result, safe=False)
        return JsonResponse([{"error": ""}], safe=False)
        pass
    return JsonResponse([{"error": "no params: lang"}], safe=False)
    pass


@api_view(['GET'])
def pagedoc_list(request):
    """从数据库获取帮助文档"""
    if request.method == 'GET':
        pages = PageDoc.objects.all().annotate(docTitle=Max('pagedoc__title'))

        return JsonResponse(list(pages.values()), safe=False)


@api_view(['GET'])
def page_revision_list(request):
    """从数据库获取文章版本"""
    if request.method == 'GET':
        pageid = request.query_params.get('pageid', None)
        if pageid is None:
            return JsonResponse([{"error": "no pageid params"}], safe=False)
        else:
            revisions = PageRevision.objects.all().filter(pageid=pageid).order_by('-timestamp')
            return JsonResponse(list(revisions.values()), safe=False)
    pass


@api_view(['GET'])
def contributor(request):
    """从数据库获取贡献者"""
    if request.method == 'GET':
        user_id = request.query_params.get('id', None)
        if user_id is None:
            return JsonResponse([{"error": "no pageid params"}], safe=False)
        else:
            user = Contributor.objects.all().filter(id=user_id)
            serializer = ContributorSerializer(user, many=True)
            return JsonResponse(serializer.data, safe=False)
            # 'safe=False' for objects serialization
    pass


@api_view(['POST'])
def pull_format_page_list(request):
    """获取需要修正文案格式的页面"""

    def getRes(p):
        is_able_format = bot_format.is_able_format(p)
        newText = p.text
        if is_able_format:
            newText = bot_format.format_str(newText)
        return {
            "title": p.title(),
            "able": is_able_format and p.text != newText,
            "oldText": p.text,
            "newText": newText,
            "latest_timestamp": p.latest_revision.timestamp
        }

    if request.method == 'POST':
        params = json.loads(request.body)
        model = params.get('model', 3)
        result = []
        if model == 1:
            pages = bot_wiki.getRecentPages()
            for page in pages:
                r = getRes(page)
                result.append(r)
            return JsonResponse(result, safe=False)
        elif model == 2:
            pages = bot_wiki.getAllPages()
            for page in pages:
                r = getRes(page)
                result.append(r)
            return JsonResponse(result, safe=False)
        elif model == 3:
            pagename = params.get('title', None)
            if pagename is not None:
                page = bot_wiki.getpage(pagename)
                r = getRes(page)
                result.append(r)
                return JsonResponse(result, safe=False)

    return JsonResponse([{"error": "no pageid params"}], safe=False)
    pass


@api_view(['POST'])
def updatePage(request):
    """更新页面"""
    if request.method == 'POST':
        data = json.loads(request.body)
        if data is not None:
            result = []
            for item in data:
                title = item.get('title', None)
                text = item.get('text', None)
                if title and text:
                    bot_wiki.update_text(title, text)
                    result.append(title)
                    print("update page:", title)
                    pass
            return JsonResponse(result, safe=False)
    return JsonResponse([{"error": "no pageid params"}], safe=False)
    pass


@api_view(['POST'])
def loginWiki(request):
    """登录wiki站点"""
    if request.method == 'POST':
        bot_wiki.loginBot()
        return JsonResponse([{"msg": "Login success!"}], safe=False)
    return JsonResponse([{"error": ""}], safe=False)


@api_view(['GET'])
def logoutWiki(request):
    """退出wiki站点"""
    if request.method == 'GET':
        bot_wiki.logoutBot()
        return JsonResponse([{"msg": "Logout success!"}], safe=False)
    return JsonResponse([{"error": ""}], safe=False)
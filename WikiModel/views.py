from django.shortcuts import render
from django.http.response import JsonResponse
from django.db.models import Max

from WikiModel.models import Page, PageRevision, Contributor, PageDoc
from WikiModel.serializers import ContributorSerializer
from rest_framework.decorators import api_view

import WikiModel.wikisite.bot_format as bot_format


@api_view(['GET', 'POST', 'DELETE'])
def page_list(request):
    """页面列表"""
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

@api_view(['GET'])
def pagedoc_list(request):
    """帮助文档"""
    if request.method == 'GET':
        pages = PageDoc.objects.all().annotate(docTitle=Max('pagedoc__title'))

        return JsonResponse(list(pages.values()), safe=False)

@api_view(['GET'])
def page_revision_list(request):
    """文章版本"""
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

@api_view(['GET'])
def pull_format_page_list(request):
    """获取需要修正文案格式的页面"""
    if request.method == 'GET':
        pagename = request.query_params.get('title', None)
        if pagename is not None:
            p = bot_format.getpage(pagename)
            result = {
                "title": p.title(),
                "is_able_format": bot_format.is_able_format(p),
                "text": p.text
            }
            return JsonResponse(result, safe=False)

    return JsonResponse([{"error": "no pageid params"}], safe=False)


    pass
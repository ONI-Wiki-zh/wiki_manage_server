from django.shortcuts import render
from django.http.response import JsonResponse
from django.db.models import Max

from WikiModel.models import Page, PageRevision, Contributor, PageDoc
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def page_list(request):
    """页面列表"""
    if request.method == 'GET':
        pages = Page.objects.all()

        # 根据ns查询页面列表
        ns = request.query_params.get('ns', None)
        if ns is not None:
            pages = Page.objects.filter(ns=ns)
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
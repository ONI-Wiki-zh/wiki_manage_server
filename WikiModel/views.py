from django.shortcuts import render
from django.http.response import JsonResponse
from django.db.models import Max

from WikiModel.models import Page, PageRevision, Contributor
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def page_list(request):
    if request.method == 'GET':
        pages = Page.objects.all()

        # 根据ns查询页面列表
        ns = request.query_params.get('ns', None)
        if ns is not None:
            pages = Page.objects.filter(ns=ns)
        res = pages.all().annotate(latest_timestamp=Max('pagerevision__timestamp'))\
            .annotate(contributorId=Max("pagerevision__contributor__id"))\
            .annotate(contributorName=Max("pagerevision__contributor__user_name"))\
            .annotate(contributorIP=Max("pagerevision__contributor__user_ip"))\
            .annotate(comment=Max("pagerevision__comment"))

        return JsonResponse(list(res.values()), safe=False)
        # 'safe=False' for objects serialization

from django.shortcuts import render
from django.http.response import JsonResponse
from WikiModel.models import Page
from WikiModel.serializers import PageSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def page_list(request):
    if request.method == 'GET':
        pages = Page.objects.all()

        # 根据ns查询页面列表
        ns = request.query_params.get('ns', None)
        if ns is not None:
            pages = Page.objects.filter(ns=ns)
        serializer = PageSerializer(pages, many=True)
        return JsonResponse(serializer.data, safe=False)
        # 'safe=False' for objects serialization
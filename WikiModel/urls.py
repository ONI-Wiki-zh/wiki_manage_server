from WikiModel import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^api/pages$', views.page_list),    #页面查询
    re_path(r'^api/pagestatus', views.page_status),    #页面状态查询
    re_path(r'^api/pagesdoc$', views.pagedoc_list),    #页面帮助文档查询
    re_path(r'^api/pagerevision', views.page_revision_list),    #文章历史版本查询
    re_path(r'^api/contributor', views.contributor),    #贡献者查询
    re_path(r'^api/pullFormatPage', views.pull_format_page_list),    #拉取需要格式修正的页面
    re_path(r'^api/updatepage', views.updatePage),    #更新页面
    re_path(r'^api/loginWiki', views.loginWiki),    #登录wiki站点
    re_path(r'^api/logoutWiki', views.logoutWiki),    #退出wiki站点
    # re_path(r'^api/pages/(?P<pk>[0-9]+)$', views.page_list),
    # re_path(r'^api/pages/published$', views.tutorial_list_published)
]

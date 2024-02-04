from WikiModel import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^api/pages$', views.page_list),    #页面查询
    # re_path(r'^api/pages/(?P<pk>[0-9]+)$', views.page_list),
    # re_path(r'^api/pages/published$', views.tutorial_list_published)
]

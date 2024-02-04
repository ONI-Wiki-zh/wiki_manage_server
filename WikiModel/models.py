from django.db import models
# Create your models here.


class WikiNamespaces(models.Model):
    """wiki命名空间"""
    key = models.IntegerField(primary_key=True)
    case = models.CharField(max_length=100)
    text = models.CharField(max_length=256)


class Page(models.Model):
    """页面"""
    page_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256, null="")
    ns = models.IntegerField(max_length=10000, null=-100)
    redirect_title = models.CharField(max_length=1000, null="")


class PageEmbedin(models.Model):
    """嵌入链接"""
    page_id = models.IntegerField()
    embeddin_page_id = models.IntegerField()


class PageRevision(models.Model):
    """页面历史版本"""
    page_id = models.IntegerField(primary_key=True)
    origin_id = models.IntegerField()
    sha1 = models.CharField(max_length=41)
    timestamp = models.CharField(max_length=20)
    time = models.TimeField()
    format = models.CharField(max_length=20)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    user_id = models.CharField(max_length=100, blank=True, null=True)
    user_ip = models.CharField(max_length=48, blank=True, null=True)
    comment = models.CharField(max_length=256, blank=True, null=True)
    text = models.TextField()
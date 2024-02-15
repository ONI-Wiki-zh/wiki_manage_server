from django.db import models
# Create your models here.


class WikiNamespaces(models.Model):
    """wiki命名空间"""
    key = models.IntegerField(primary_key=True)
    case = models.CharField(max_length=100)
    text = models.CharField(max_length=256)


class Page(models.Model):
    """页面"""
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256, null="")
    ns = models.IntegerField()
    redirect_title = models.CharField(max_length=1000, null="")


class PageDoc(models.Model):
    """帮助文档"""
    id = models.IntegerField(primary_key=True)
    pagedoc = models.OneToOneField('Page', on_delete=models.CASCADE)


class PageEmbedin(models.Model):
    """嵌入链接"""
    id = models.IntegerField(primary_key=True)
    embeddin = models.IntegerField()


class PageStatus(models.Model):
    """页面"""
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256, null="")
    ns = models.IntegerField()
    target = models.CharField(max_length=20, null="")
    latest_timestamp = models.CharField(max_length=20)
    outdated = models.BooleanField()
    noneTargetLangPage = models.BooleanField()
    onewayLangLink = models.BooleanField()
    multiBackLangLinks = models.BooleanField()


class PageRevision(models.Model):
    """页面历史版本"""
    id = models.IntegerField(primary_key=True)
    origin = models.IntegerField()
    pageid = models.ForeignKey('Page', on_delete=models.CASCADE)
    sha1 = models.CharField(max_length=41)
    timestamp = models.CharField(max_length=20)
    time = models.TimeField()
    format = models.CharField(max_length=20)
    contributor = models.ForeignKey('Contributor', on_delete=models.CASCADE)
    comment = models.CharField(max_length=256, blank=True, null=True)
    text = models.TextField()


class Contributor(models.Model):
    """贡献者"""
    id = models.CharField(primary_key=True, max_length=256)
    user_name = models.CharField(max_length=256, blank=True, null=True)
    user_ip = models.CharField(max_length=48, blank=True, null=True)

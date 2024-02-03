from django.db import models
# Create your models here.


class WikiNamespaces(models.Model):
    key = models.IntegerField(primary_key=True)
    case = models.CharField(max_length=100)
    text = models.CharField(max_length=256)


class Page(models.Model):
    page_id = models.IntegerField()
    title = models.CharField(max_length=256, null="")
    ns = models.IntegerField(max_length=10000, null=-100)
    redirect_title = models.CharField(max_length=1000, null="")


class PageRevision(models.Model):
    page_id = models.IntegerField(primary_key=True)
    origin_id = models.IntegerField()
    sha1 = models.CharField(max_length=41)
    timestamp = models.CharField(max_length=20)
    time = models.TimeField()
    format = models.CharField(max_length=20)
    user_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    user_ip = models.CharField(max_length=48)
    comment = models.CharField(max_length=256)
    text = models.TextField()
import json
import os.path
from django.core.management.base import BaseCommand
from WikiModel.models import Page, PageRevision, Contributor
from django.conf import settings
from django.db import connection
from datetime import datetime


def saveContributor(page):
    # 文章历史版本
    data = page.get('revision', None)
    if data is None:
        return
    revisions = []
    if type(data) == list:
        revisions = data
    else:
        revisions.append(data)
    for revision in revisions:
        contributor = revision.get('contributor', None)
        user_ip = contributor.get('ip', None)
        user_id = contributor.get('id', None)
        if user_id is None:
            if user_ip is None:
                user_id = "0.0.0.0"
            else:
                user_id = user_ip
        model_instance = Contributor(
            id = user_id,
            user_name = contributor.get('username', None),
            user_ip = user_ip
        )
        model_instance.save()

def savePage(page):
    # 文章概要
    redirect_title = ""
    redirect = page.get('redirect', None)
    if redirect is not None:
        redirect_title = redirect.get('@title', "")
    model_instance = Page(
        id=page['id'],
        title=page['title'],
        ns=page['ns'],
        redirect_title=redirect_title,
    )
    model_instance.save()
    pass


def savePageRevision(page):
    # 文章历史版本
    data = page.get('revision', None)
    if data is None:
        return
    revisions = []
    if type(data) == list:
        revisions = data
    else:
        revisions.append(data)
    for revision in revisions:
        contributor = revision.get('contributor', None)
        user_ip = contributor.get('ip', None)
        user_id = contributor.get('id', None)
        if user_id is None:
            if user_ip is None:
                user_id = "0.0.0.0"
            else:
                user_id = user_ip
        model_instance = PageRevision(
            id=revision['id'],
            origin=revision['origin'],
            pageid=Page.objects.filter(id=page['id']).first(),
            sha1=revision['sha1'],
            timestamp=revision['timestamp'],
            time=datetime.strptime(revision['timestamp'], "%Y-%m-%dT%H:%M:%SZ"),
            format=revision['format'],
            contributor=Contributor.objects.filter(id=user_id).first(),
            comment=revision.get('comment', None),
            text=revision['text'],
        )
        model_instance.save()
    pass


class Command(BaseCommand):
    help = 'Load data from JSON file into SQLite'

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, 'data_input', 'zhoxygennotincluded_pages_current_bot_20240127.json')
        with open(file_path, 'r') as f:
            data = json.load(f)
        mediawiki = data.get('mediawiki', None)
        if mediawiki is None:
            self.stdout.write('No MediaWiki Data')
            return
        pages = mediawiki.get('page', None)
        if pages is None:
            self.stdout.write('No Page Data')
            return
        # 重置表
        table_name = Page._meta.db_table  # 获取表名
        with connection.cursor() as cursor:
            cursor.execute(f'DELETE FROM {table_name};')
        table_name = PageRevision._meta.db_table  # 获取表名
        with connection.cursor() as cursor:
            cursor.execute(f'DELETE FROM {table_name};')
        table_name = Contributor._meta.db_table  # 获取表名
        with connection.cursor() as cursor:
            cursor.execute(f'DELETE FROM {table_name};')
        # 载入数据
        for page in pages:
            saveContributor(page)
            savePage(page)
        for page in pages:
            savePageRevision(page)

        self.stdout.write('wiki xml data loaded!')

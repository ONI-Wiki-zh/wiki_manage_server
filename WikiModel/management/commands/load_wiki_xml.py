import json
import os.path
from django.core.management.base import BaseCommand
from WikiModel.models import Page, PageRevision
from django.conf import settings
from django.db import connection
from datetime import datetime


def is_array(var):
    return isinstance(var, (list, np.ndarray))


def savePage(page):
    # 文章概要
    redirect_title = ""
    redirect = page.get('redirect', None)
    if redirect is not None:
        redirect_title = redirect.get('@title', "")
    model_instance = Page(
        page_id=page['id'],
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
        model_instance = PageRevision(
            page_id=revision['id'],
            origin_id=revision['origin'],
            sha1=revision['sha1'],
            timestamp=revision['timestamp'],
            time=datetime.strptime(revision['timestamp'], "%Y-%m-%dT%H:%M:%SZ"),
            format=revision['format'],
            user_name=contributor.get('username', None),
            user_id=contributor.get('id', None),
            user_ip=contributor.get('ip', None),
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
        # 载入数据
        for page in pages:
            if not Page.objects.filter(page_id=page['id']).exists():
                savePage(page)
                savePageRevision(page)

        self.stdout.write('wiki xml data loaded!')

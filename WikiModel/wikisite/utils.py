#-*- encoding:utf-8 -*-
import os.path as path
import os
import pathlib
from typing import List

import pywikibot
import pywikibot.data.api


def get_tags(site):
    assert isinstance(site, pywikibot.APISite)
    r = pywikibot.data.api.Request(
        site, parameters={"action": "query", "list": "tags"})
    res = r.submit()
    if 'query' in res and 'tags' in res['query']:
        tags = res['query']['tags']
        return [t['name'] for t in tags]
    return []


def _get_try_tags_save_func():
    sites_tags = {}

    def inner(p: pywikibot.Page, tags: List[str], *args, **kwargs):
        if p.site not in sites_tags:
            sites_tags[p.site] = get_tags(p.site)
        available_tags = [t for t in tags if t in sites_tags[p.site]]
        return p.save(*args, tags=available_tags, **kwargs)

    return inner


try_tags_save = _get_try_tags_save_func()


def to_camel(s):
    init, *temp = s.split('_')
    return ''.join([init.lower(), *map(str.title, temp)])


def to_cap(s):
    return ''.join([w.title() for w in s.split('_')])


def split_file_name(filename: str):
    return pathlib.Path(filename).stem, pathlib.Path(filename).suffix


if __name__ == '__main__':
    pass
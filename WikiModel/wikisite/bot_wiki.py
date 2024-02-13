import os
import typing
import datetime
import pywikibot
import dateutil.parser

from WikiModel.wikisite import utils


def get_recent_pages(
        site: pywikibot.Site,
        recent_seconds: typing.Optional[int]) -> typing.List[pywikibot.Page]:
    """获取最近更新的页面"""
    # copy from: Botnotincluded
    if not recent_seconds:
        if "RC_IN_SECONDS" in os.environ:
            recent_seconds = os.environ["RC_IN_SECONDS"]
            recent_seconds = int(recent_seconds)
        else:
            recent_seconds = 7200

    recent_page_ids = set()
    recent_pages = []
    curr_time = datetime.datetime.now(datetime.timezone.utc)
    for record in site.recentchanges(bot=False, namespaces=[0, 4, 6, 12, 14]):
        if record['type'] == 'log':
            continue
        record_time = dateutil.parser.isoparse(record['timestamp'])
        from_now = (curr_time - record_time).total_seconds()
        if from_now > recent_seconds:
            break
        if record['pageid'] not in recent_page_ids:
            recent_pages.append(pywikibot.Page(site, title=record['title']))
            recent_page_ids.add(record['pageid'])
    return recent_pages


def getpage(pagename: str):
    """获取页面"""
    Site_ONI_ZH = pywikibot.Site("zh", "oni")
    page = pywikibot.Page(Site_ONI_ZH, pagename)
    return page


def getAllPages():
    """获取所有页面"""
    Site_ONI_ZH = pywikibot.Site("zh", "oni")
    return list(Site_ONI_ZH.allpages(content=True))


def getRecentPages():
    """获取最近更新的页面"""
    Site_ONI_ZH = pywikibot.Site("zh", "oni")
    return get_recent_pages(Site_ONI_ZH, None)


def update_text(title: str, new_text: str):
    """更新页面文本"""
    Site_ONI_ZH = pywikibot.Site("zh", "oni")
    p = pywikibot.Page(Site_ONI_ZH, title)
    p.text = new_text
    utils.try_tags_save(p, ['auto-format'], summary="[[Project:格式指导|统一格式]]", watch=False)
    pass


def loginBot():
    """登录机器人账号"""
    Site_ONI_ZH = pywikibot.Site("zh", "oni")
    Site_ONI_ZH.login()


if __name__ == '__main__':
    pass
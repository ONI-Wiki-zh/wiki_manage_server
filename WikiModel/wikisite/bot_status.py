import pywikibot
from WikiModel.wikisite.constant_wiki import zh_contributors


def transform_dict(input_dict):
    result = {}
    for key in input_dict:
        for obj in input_dict[key]:
            title = obj.title()
            if title not in result:
                result[title] = {}
            result[title][key] = True
            if result[title].get("obj", None) is None:
                result[title]["obj"] = obj

    # 将没有出现在某个键的对象设为False
    for obj_title in result:
        for key in input_dict:
            if key not in result[obj_title]:
                result[obj_title][key] = False

    return result


def makePageStatus(p, target_lang):
    """生成页面状态"""
    p: pywikibot.Page
    return {
        "id": p.pageid,
        "title": p.title(),
        "ns": p.namespace().id,
        "target": target_lang,
        "latest_timestamp": p.latest_revision.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "outdated": False,
        "noneTargetLangPage": False,
        "onewayLangLink": False,
        "multiBackLangLinks": False,
    }


@DeprecationWarning
def bot_update(site: pywikibot.Site, target: pywikibot.Site):
    to_update = {
        "outdated": [],
        "non-existence": [],
        "oneway": [],
        "non-unique": [],
    }
    all_pages = list(site.allpages(content=True))
    for i, p in enumerate(all_pages):
        p: pywikibot.Page
        if i % 10 == 0:
            print(f"Page inter-lang checked: {i}/{len(all_pages)}")
        try:
            src_links = [link for link in p.langlinks() if link.site == target]
            if len(src_links) == 0:  # ignore pages with no interwiki links
                continue

            tgt_page = pywikibot.Page(src_links[0])
            if not tgt_page.exists():
                to_update["non-existence"].append(p)
                continue

            back = [link for link in tgt_page.langlinks() if link.site == site]
            if len(back) == 0:
                to_update["oneway"].append(p)
                continue

            if back[0].title != p.title():
                to_update['non-unique'].append(p)
                continue

            for r in tgt_page.revisions():
                if r.user in zh_contributors:
                    continue
                if "zh link".upper() in r.comment.upper():
                    continue
                if r.timestamp > p.latest_revision.timestamp and "版本/" not in p.title():
                    to_update["outdated"].append(p)
                break
        except pywikibot.exceptions.UnknownSiteError as e:
            msg = f"UnknownSiteError when checking {p.title()}: {str(e)}"
            print(msg)
            continue

    return to_update


def check_status(p, site, target_site):
    """检查页面的状态"""
    p: pywikibot.Page
    ps = makePageStatus(p, target_site.code)
    try:
        src_links = [link for link in p.langlinks() if link.site == target_site]
        if len(src_links) == 0:  # ignore pages with no interwiki links
            return ps

        tgt_page = pywikibot.Page(src_links[0])
        if not tgt_page.exists():
            ps["noneTargetLangPage"] = True
            return ps

        back = [link for link in tgt_page.langlinks() if link.site == site]
        if len(back) == 0:
            ps["onewayLangLink"] = True
            return ps

        if back[0].title != p.title():
            ps['multiBackLangLinks'] = True
            return ps

        for r in tgt_page.revisions():
            if r.user in zh_contributors:
                return ps
            if "zh link".upper() in r.comment.upper():
                return ps
            if r.timestamp > p.latest_revision.timestamp and "版本/" not in p.title():
                ps["outdated"] = True
            break
    except pywikibot.exceptions.UnknownSiteError as e:
        msg = f"UnknownSiteError when checking {p.title()}: {str(e)}"
        print(msg)
        return ps
    return ps
    pass


def get_pages_status(pages, target_lang: str):
    """获取碳状态更新"""
    site_ONI_ZH = pywikibot.Site("zh", "oni")
    site_target = pywikibot.Site(target_lang, "oni")
    result = []
    for p in pages:
        ps = check_status(p, site_ONI_ZH, site_target)
        result.append(ps)
    return result
    pass


if __name__ == '__main__':
    pass

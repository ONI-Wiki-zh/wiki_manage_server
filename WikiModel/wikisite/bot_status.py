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


def get_page(target_lang: str):
    Site_ONI_ZH = pywikibot.Site("zh", "oni")
    site_target = pywikibot.Site(target_lang, "oni")
    data = bot_update(Site_ONI_ZH, site_target)
    dict_page = transform_dict(data)
    result = []
    for title, item in dict_page.items():
        p = item.get("obj", None)
        if p is not None:
            result.append({
                "id": p.pageid,
                "title": title,
                "ns": p.namespace(),
                "target": target_lang,
                "outdated": item.get("outdated", False),
                "noneTargetLangPage": item.get("non-existence", False),
                "onewayLangLink": item.get("oneway", False),
                "multiBackLangLinks": item.get("non-unique", False),
            })
    return result
    pass


if __name__ == '__main__':
    pass

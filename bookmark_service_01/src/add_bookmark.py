# add_bookmark.py
import yaml
from config import BOOKMARK_CONFIG_PATH

def load_bookmarks():
    """
    从配置文件中加载书签数据。
    :return: 书签数据
    """
    try:
        with open(BOOKMARK_CONFIG_PATH, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file) or []
    except FileNotFoundError:
        return []

def get_bookmarks_groups():
    """
    获取书签分组。
    :return: 书签分组列表
    """
    bookmarks = load_bookmarks()
    return [list(group.keys())[0] for group in bookmarks]

def get_bookmarks_services(group_name):
    """
    获取分组下的书签服务。
    :param group_name: 分组名
    :return: 分组下的书签服务列表
    """
    bookmarks = load_bookmarks()
    for group in bookmarks:
        if list(group.keys())[0] == group_name:
            return [list(service.keys())[0] for service in group[group_name]]
    return []

def get_bookmarks_service(group_name, service_name):
    """
    获取分组下的指定书签服务。
    :param group_name: 分组名
    :param service_name: 服务名
    :return: 书签服务信息
    """
    bookmarks = load_bookmarks()
    for group in bookmarks:
        if list(group.keys())[0] == group_name:
            for service in group[group_name]:
                if list(service.keys())[0] == service_name:
                    return service[service_name][0]
    return None

def save_bookmarks(bookmarks):
    """
    将书签数据保存到配置文件中。
    :param bookmarks: 书签数据
    """
    with open(BOOKMARK_CONFIG_PATH, 'w', encoding='utf-8') as file:
        yaml.dump(bookmarks, file, allow_unicode=True)

def add_bookmark(group_name, service_name, abbr=None, url=None):
    """
    添加新的书签。
    :param group_name: 分组名
    :param service_name: 书签名
    :param abbr: 缩写名
    :param url: 链接名
    """
    bookmarks = load_bookmarks()
    group_found = False
    for group in bookmarks:
        if list(group.keys())[0] == group_name:
            group_found = True
            service = {
                service_name: [
                    {
                        'abbr': abbr if abbr else '',
                        'href': url if url else ''
                    }
                ]
            }
            group[group_name].append(service)
            break
    if not group_found:
        new_group = {
            group_name: [
                {
                    service_name: [
                        {
                            'abbr': abbr if abbr else '',
                            'href': url if url else ''
                        }
                    ]
                }
            ]
        }
        bookmarks.append(new_group)
    save_bookmarks(bookmarks)

def add_bookmark_groups(group_name):
    """
    添加新的书签分组。
    :param group_name: 分组名
    """
    bookmarks = load_bookmarks()
    group_exists = any(list(group.keys())[0] == group_name for group in bookmarks)
    if not group_exists:
        new_group = {group_name: []}
        bookmarks.append(new_group)
        save_bookmarks(bookmarks)
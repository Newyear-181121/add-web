import yaml
import logging
from config import BOOKMARK_CONFIG_PATH

# 设置日志记录器
logger = logging.getLogger(__name__)

def load_bookmarks():
    """
    从配置文件中加载书签数据。
    :return: 书签数据
    """
    logger.debug(f"加载书签配置文件: {BOOKMARK_CONFIG_PATH}")
    try:
        with open(BOOKMARK_CONFIG_PATH, 'r', encoding='utf-8') as file:
            bookmarks = yaml.safe_load(file) or []
            logger.info(f"成功加载 {len(bookmarks)} 个书签分组")
            return bookmarks
    except FileNotFoundError:
        logger.warning(f"配置文件不存在: {BOOKMARK_CONFIG_PATH}，返回空列表")
        return []
    except Exception as e:
        logger.error(f"加载书签配置失败: {str(e)}", exc_info=True)
        return []

def get_bookmarks_groups():
    """
    获取书签分组。
    :return: 书签分组列表
    """
    logger.debug("获取所有书签分组")
    bookmarks = load_bookmarks()
    groups = [list(group.keys())[0] for group in bookmarks]
    logger.info(f"找到 {len(groups)} 个书签分组")
    return groups

def get_bookmarks_services(group_name):
    """
    获取分组下的书签服务。
    :param group_name: 分组名
    :return: 分组下的书签服务列表
    """
    logger.debug(f"获取分组 '{group_name}' 下的所有服务")
    bookmarks = load_bookmarks()
    for group in bookmarks:
        if list(group.keys())[0] == group_name:
            services = [list(service.keys())[0] for service in group[group_name]]
            logger.info(f"分组 '{group_name}' 下有 {len(services)} 个服务")
            return services
    logger.warning(f"未找到分组: {group_name}")
    return []

def get_bookmarks_service(group_name, service_name):
    """
    获取分组下的指定书签服务。
    :param group_name: 分组名
    :param service_name: 服务名
    :return: 书签服务信息
    """
    logger.debug(f"获取分组 '{group_name}' 下的服务 '{service_name}'")
    bookmarks = load_bookmarks()
    for group in bookmarks:
        if list(group.keys())[0] == group_name:
            for service in group[group_name]:
                if list(service.keys())[0] == service_name:
                    logger.info(f"成功找到服务: {service_name}")
                    return service[service_name][0]
    logger.warning(f"未找到服务: {service_name} 在分组 {group_name} 中")
    return None

def save_bookmarks(bookmarks):
    """
    将书签数据保存到配置文件中。
    :param bookmarks: 书签数据
    """
    logger.debug(f"保存书签配置到: {BOOKMARK_CONFIG_PATH}")
    try:
        with open(BOOKMARK_CONFIG_PATH, 'w', encoding='utf-8') as file:
            yaml.dump(bookmarks, file, allow_unicode=True)
        logger.info(f"成功保存 {len(bookmarks)} 个书签分组到配置文件")
        return True
    except Exception as e:
        logger.error(f"保存书签配置失败: {str(e)}", exc_info=True)
        return False

def add_bookmark(group_name, service_name, abbr=None, url=None):
    """
    添加新的书签。
    :param group_name: 分组名
    :param service_name: 书签名
    :param abbr: 缩写名
    :param url: 链接名
    """
    logger.info(f"添加新书签: {service_name} 到分组 {group_name}")
    logger.debug(f"书签详情: abbr={abbr}, url={url}")
    
    bookmarks = load_bookmarks()
    group_found = False
    
    # 检查是否已存在相同名称的书签
    for group in bookmarks:
        if list(group.keys())[0] == group_name:
            group_found = True
            # 检查是否已存在相同名称的服务
            for service in group[group_name]:
                if list(service.keys())[0] == service_name:
                    logger.warning(f"书签已存在: {service_name}，将被覆盖")
                    # 移除现有服务
                    group[group_name].remove(service)
                    break
            
            # 添加新服务
            service = {
                service_name: [
                    {
                        'abbr': abbr if abbr else '',
                        'href': url if url else ''
                    }
                ]
            }
            group[group_name].append(service)
            logger.info(f"成功添加书签: {service_name} 到现有分组 {group_name}")
            break
    
    if not group_found:
        # 创建新分组并添加服务
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
        logger.info(f"成功添加书签: {service_name} 到新分组 {group_name}")
    
    return save_bookmarks(bookmarks)

def add_bookmark_groups(group_name):
    """
    添加新的书签分组。
    :param group_name: 分组名
    """
    logger.info(f"添加新书签分组: {group_name}")
    bookmarks = load_bookmarks()
    group_exists = any(list(group.keys())[0] == group_name for group in bookmarks)
    
    if group_exists:
        logger.warning(f"分组已存在: {group_name}，不执行操作")
        return False
    else:
        new_group = {group_name: []}
        bookmarks.append(new_group)
        logger.info(f"成功添加新分组: {group_name}")
        return save_bookmarks(bookmarks)

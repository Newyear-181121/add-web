import change_config
from config import BOOKMARK_CONFIG_PATH 
import logging
import os

# 配置日志
# logging.basicConfig(
    # level=logging.DEBUG,
    # format='[%(filename)s] - %(asctime)s - %(name)s - %(levelname)s - %(message)s',
    # force=True  # 强制覆盖之前的配置
# )
logger = logging.getLogger(__name__)


# 切换配置文件路径
OTHER_BOOKMARK_CONFIG_FILE = base_dir = os.path.dirname(__file__) + '/configs/other/next_setting.yaml'

# 翻页下一页：
# 修改配置文件，索引加一，活动文件修改成对应的文件，并将活动文件的内容复制到到标准配置文件
def change_page_config(next=True, type="bookmarks"):
    """
    修改书签配置到下一页或上一页
    
    Args:
        next: true表示下一页，false表示上一页
        type: 配置类型，默认为 "bookmarks", ”services", "settings"
    
    Returns:
        str: 操作结果消息
    """
    # 1. 获取当前的配置索引,和活动文件
    current_bookmarks_index = change_config.get_config_file_content(OTHER_BOOKMARK_CONFIG_FILE, type, "index")
    current_bookmarks_active = change_config.get_config_file_content(OTHER_BOOKMARK_CONFIG_FILE, type, "action") 
    # 2. 修改索引和活动文件， 索引达到最大时，索引归1
    current_bookmarks_files = change_config.get_config_file_content(OTHER_BOOKMARK_CONFIG_FILE, type, "files")
    target_file = change_config.get_config_file_content(OTHER_BOOKMARK_CONFIG_FILE, type, "target")
    if next:
        if current_bookmarks_index + 1 > len(current_bookmarks_files):
            new_index = 1
        else:
            new_index = current_bookmarks_index + 1
    else:
        if current_bookmarks_index - 1 < 0:
            new_index = len(current_bookmarks_files) 
        else:
            new_index = current_bookmarks_index - 1
    new_bookmarks_active = current_bookmarks_files[new_index - 1]
    # 3. 修改配置文件
    change_config.change_config_file_content(OTHER_BOOKMARK_CONFIG_FILE, type, "index", new_index)
    change_config.change_config_file_content(OTHER_BOOKMARK_CONFIG_FILE, type, "action", new_bookmarks_active)

    try:
        current_bookmarks_active = change_config.get_abs_path(current_bookmarks_active, "/other/" + type)
        # 4. 确保保存的活动配置文件是最新的
        change_config.copy_config_file_content(target_file, current_bookmarks_active)

        # 4. 将活动文件的内容复制到标准配置文件
        new_bookmarks_active = change_config.get_abs_path(new_bookmarks_active, "/other/" + type)
        change_config.copy_config_file_content(new_bookmarks_active, target_file)
    except Exception as e:
        logger.error(f"保存活动配置文件时出错: {e}")
    # 三元运算符
    return "下一页" if next else "上一页"
    

# 在公共配置中显示总页数和当前页数
def set_page_info():
    current_index = change_config.get_config_file_content(change_config.OTHER_BOOKMARK_CONFIG_PATH, "bookmarks", "index")
    # todo: 
    change_config.change_config_file_content(BOOKMARK_CONFIG_PATH, "bookmarks", "total", )

# 开始执行
if __name__ == '__main__':
    change_page_config()
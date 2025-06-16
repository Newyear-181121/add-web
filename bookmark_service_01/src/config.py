# config.py
import os
import yaml
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='[config] - %(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 书签配置文件的路径
BOOKMARK_CONFIG_PATH = os.path.join(os.getcwd(), '/app/configs/bookmarks.yaml')
BOOKMARK_DIRS = os.path.dirname(BOOKMARK_CONFIG_PATH)

def get_all_filenames(path=BOOKMARK_DIRS):
    """
    获取指定路径下的所有文件的文件名。
    :param path: 指定的路径
    :return: 文件名列表
    """
    if not path:
        print("路径为空,使用默认配置文件！")
        path = BOOKMARK_DIRS
    # 确保路径是绝对路径
    path = os.path.abspath(path)  
    if not os.path.exists(path):
        print(f"路径不存在: {path}")
        return []

    try:
        if os.path.exists(path) and os.path.isdir(path):
            return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return []
    except Exception as e:
        print(f"错误的获取文件名列表: {e}")
        return []

def get_yaml_file_content(dirs=BOOKMARK_DIRS, file_name="bookmarks.yaml"):
    """
    获取指定文件路径下指定 YAML 文件的内容。
    :param dirs: 指定的文件路径
    :param file_name: 默认为 bookmarks.yaml
    :return: YAML 文件内容，如果读取失败则返回 None
    """
    try:
        # 判断 dirs 路径是否存在，如果不存在则使用默认配置路径  
        if not dirs:
            dirs = BOOKMARK_DIRS
            logger.warning("目录路径为空, 使用默认配置目录 {dirs}")
        # 判断 file_name 是否存在
        if not file_name:
            file_name = "bookmarks.yaml"
            logger.warning("文件名不存在, 使用默认文件名 {file_name}")
        # 拼接完整的文件路径
        file_path = os.path.join(dirs, file_name)


        if os.path.exists(file_path) and file_path.endswith(('.yaml', '.yml')):
            with open(file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        return None
    except Exception as e:
        print(f"错误的获取文件内容: {e}")
        return None
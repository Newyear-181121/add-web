# config.py
import os

# 书签配置文件的路径
BOOKMARK_CONFIG_PATH = os.path.join(os.getcwd(), '/app/configs/bookmarks.yaml')
BOOKMARK_DIRS = os.path.dirname(BOOKMARK_CONFIG_PATH)

# 新增配置文件管理相关路径
CONFIG_DIR = os.path.dirname("/app/configs")  # 配置文件目录
TARGET_CONFIG_PATH = os.path.join(BOOKMARK_DIRS, "active_config.yaml")  # 目标配置文件路径
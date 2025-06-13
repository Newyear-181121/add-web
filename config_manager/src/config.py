import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 配置文件目录
CONFIG_DIR = os.path.join(BASE_DIR, "configs")

# 确保配置目录存在
os.makedirs(CONFIG_DIR, exist_ok=True)

# 目标配置文件路径（当前活动配置）
TARGET_CONFIG_PATH = os.path.join(BASE_DIR, "active_config.json")    
# change_config.py
import os
import yaml
import logging
import sys

# 配置日志
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='[config] - %(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     force=True  # 强制覆盖之前的配置
# )
logger = logging.getLogger(__name__)


def get_abs_path(file_path, types=""):
    """
    获取文件的绝对路径
    Args:
        file_path: 相对路径或绝对路径
    
    Returns:
        str: 文件的绝对路径
    """
    # 开发指定相对路径的文件夹，
    path = "configs" + types
    # 实际容器中使用的相对路径
    # 容器中的路径：/app/configs/other/next_setting.yaml
    # path = "configs/other"
    logging.debug(f"获取 {file_path} 文件的绝对路径! ")
    if os.path.isabs(file_path):
        logging.debug(f"{file_path} 是绝对路径! ")
        return file_path
    else:
        # 获取当前脚本所在目录
        base_dir = os.path.dirname(__file__)
        base_dir = os.path.join(base_dir, path)
        result = os.path.join(base_dir, file_path)
        logging.debug(f"{file_path} 是相对路径! 转换为绝对路径: {result}")
        return result



# 获取指定配置文件中指定类型的 子配置项的值
def get_config_file_content(file_path, type, config_item):
    """
    从指定配置文件中获取指定类型和配置项的值
    
    参数:
        config_file_path (str): 配置文件的路径
        type (str): 配置文件中的类型分类， 例如 'bookmarks'
        config_item (str): 需要获取的具体配置项名称
        
    返回:
        配置项的值，如果不存在则返回None
    """
    config_file_path = get_abs_path(file_path)
    filename = os.path.basename(config_file_path)
    logging.debug(f"获取配置文件内容: {filename}, 类型: {type}, 配置项: {config_item}")
    try:
        with open(config_file_path, 'r', encoding='utf-8') as f:
            # 读取文件
            config_file_content = yaml.safe_load(f)
            # 返回读取的指定值
            result = config_file_content[type][config_item]
            logging.debug(f"获取配置文件内容: {filename}, 类型: {type}, 配置项: {config_item}, 成功！ 值: {result}")
            return result
        # yaml 的配置，使用不同的配置，加载出来的是 dist和list， 使用了 - 开头加载出来的就是  list
    except Exception as e:
        logger.error(f"获取配置文件内容失败！{config_file_path} {e}")


# 修改配置文件中 指定类型 的配置项的值
def change_config_file_content(file_path, type, config_item, config_value):
    config_file_path = get_abs_path(file_path)
    filename = os.path.basename(config_file_path)
    logging.debug(f"修改配置文件内容: {filename}, 类型: {type}, 配置项: {config_item},  新值: {config_value}")
    try:
        old_value = {}
        with open(config_file_path, 'r', encoding='utf-8') as f:
            # 指定使用 FullLoader 加载器，这是一种安全的加载方式，可以防止潜在的代码执行漏洞
            config_file_content = yaml.load(f, Loader=yaml.FullLoader)
            # 修改指定配置项的值
            old_value = config_file_content[type][config_item]
            config_file_content[type][config_item] = config_value  
        # 将修改后的内容写回文件
        with open(config_file_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_file_content, f, allow_unicode=True)
        
        logging.debug(f"修改配置文件内容: {filename}, 类型: {type}, 配置项: {config_item},  新值: {config_value} 成功！ 原值：{old_value}")
    except Exception as e:
        logger.error(f"修改配置文件失败！{config_file_path} {e}")


# 复制指定配置到指定文件
# 获取配置文件1内容，覆盖配置文件2的内容。
def copy_config_file_content(config_file_path_1, config_file_path_2):
    try:
        file1 = get_abs_path(config_file_path_1)
        file2 = get_abs_path(config_file_path_2)
        # 检查文件是否存在
        if not os.path.exists(file1):
            logger.error(f"源配置文件不存在: {file1}")
            return
        if not os.path.exists(os.path.dirname(file2)):
            logger.error(f"目标配置文件目录不存在: {os.path.dirname(file2)}")
            return
        with open(file1, 'r', encoding='utf-8') as f:
            config_file_content_1 = yaml.load(f, Loader=yaml.FullLoader)
        with open(file2, 'w', encoding='utf-8') as f:
            # allow_unicode=True 可以让 PyYAML 输出中文而不是 \u 形式
            yaml.dump(config_file_content_1, f, allow_unicode=True)
        logger.info(f"复制配置文件成功！{file1} -> {file2}")
    except Exception as e:
        logger.error(f"复制配置文件失败！{file1} -> {file2} {e}")

# 复制多个配置文件的内容到指定文件：
def copy_configs_file_content(config_file_path_1, *config_file_paths):
    """
        复制多个配置文件的内容到指定文件：
        1. 遍历所有传入的配置文件路径
        2. 读取每个配置文件的内容
        3. 合并所有配置文件的内容
        4. 将合并后的内容写入目标文件
        注意：当前实现存在逻辑问题，all_file_content被设计为列表但yaml.load可能返回字典，
        直接extend会导致数据结构错误，需要根据实际数据结构调整合并方式
    """
    # 读取多个配置文件的内容，合并到指定文件
    all_file_content = []
    for path in config_file_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                current_file_content = yaml.load(f, Loader=yaml.FullLoader)
                # 合并多个配置文件的内容
                all_file_content.extend(current_file_content)
                logger.debug(f"读取配置文件成功！{path} 成功！")
        except Exception as e:
            logger.error(f"读取配置文件失败！{path} {e}")
    if not all_file_content:
        try: 
            with open(config_file_path_1, 'w', encoding='utf-8') as f:
                yaml.dump([], f)
                logger.debug(f"清空配置文件成功！{config_file_path_1}")
                yaml.dump(all_file_content, f, encoding='utf-8')
                logger.debug(f"写入配置文件成功！{config_file_path_1}")
        except Exception as e:
            logger.error(f"清空配置文件失败！{config_file_path_1} {e}")
        return


# 开始执行
if __name__ == '__main__':
    print("被其他脚本调用时，也会执行这里的方法")
    logging.debug("debug 信息")
    logging.info("info 信息")
    logging.warning("warning 信息")
    logging.error("error 信息")
#     script_path = os.path.abspath(sys.argv[0])
#     logger.debug(f"脚本路径: {script_path}")
#     # 获取配置文件内容
#     config_file_path = OTHER_BOOKMARK_CONFIG_PATH
#     config_item = 'active'
#     config_type = 'bookmarks'
#     active_file = get_config_file_content(config_file_path, config_type, config_item)
#     logger.info(f"当前活动文件: {active_file}")

#     # 修改配置文件内容
#     new_active_file = 'new_bookmarks.yaml'
    # change_config_file_content(config_file_path, config_item, new_active_file)

    # 复制配置文件内容
    # copy_config_file_content(config_file_path, os.path.join(OTHER_BOOKMARK_DIRS, new_active_file))



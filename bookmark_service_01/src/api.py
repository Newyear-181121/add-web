import logging
from flask import jsonify, request
from add_bookmark import load_bookmarks, add_bookmark, save_bookmarks
from config import get_all_filenames, get_yaml_file_content

# 配置日志
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='[api] - %(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
logger = logging.getLogger(__name__)

def api_get_bookmarks():
    """
    处理获取书签的分组API请求。
    :return: 书签数据的JSON响应
    """
    logger.info("收到获取书签列表的请求")
    
    try:
        bookmarks = load_bookmarks()
        logger.info(f"成功加载 {len(bookmarks)} 个书签分组")
        return jsonify(bookmarks)
    except Exception as e:
        logger.error(f"获取书签列表失败: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to load bookmarks', 'details': str(e)}), 500

def api_add_bookmark():
    """
    处理添加书签的 API 请求。
    :return: 操作结果的JSON响应
    """
    logger.info("收到添加书签的请求")
    
    try:
        data = request.get_json()
        logger.debug(f"请求数据: {data}")
        
        group_name = data.get('group_name')
        service_name = data.get('service_name')
        abbr = data.get('abbr')
        url = data.get('url')
        
        if group_name and service_name and url:
            add_bookmark(group_name, service_name, abbr, url)
            logger.info(f"成功添加书签: {service_name} 到分组 {group_name}")
            return jsonify({'message': 'Bookmark added successfully', 'code': 200})
        else:
            logger.warning("添加书签失败: 缺少必要字段")
            return jsonify({'error': 'Missing required fields'}), 400
    except Exception as e:
        logger.error(f"添加书签时发生错误: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to add bookmark', 'details': str(e)}), 500

def api_save_bookmarks():
    """
    处理保存书签的 API 请求。
    :return: 操作结果的JSON响应
    """
    logger.info("收到保存书签的请求")
    
    try:
        data = request.get_json()
        logger.debug(f"请求数据: {data}")
        
        save_bookmarks(data)
        logger.info("成功保存书签配置")
        return jsonify({'message': '书签添加成功！', 'code': 200})
    except Exception as e:
        logger.error(f"保存书签配置失败: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to save bookmarks', 'details': str(e)}), 500


def api_get_configs(dir):
    """
    获取指定目录下的所有配置文件。
    :param dir: 指定的目录路径
    :return: 配置文件列表的JSON响应
    """
    logger.info(f"收到获取配置文件列表的请求，目录: {dir}")
    
    try:
        # 获取指定目录下的所有文件名
        filenames = get_all_filenames(dir)
        
        if not filenames:
            logger.info("没有找到任何配置文件")
            return jsonify({'message': '没有找到配置文件。', 'files': []})
        
        logger.info(f"成功获取 {len(filenames)} 个配置文件")
        return jsonify({'files': filenames, 'code': 200})
    except Exception as e:
        logger.error(f"获取配置文件列表失败: {str(e)}", exc_info=True)
        return jsonify({'error': '错误的获取配置文件列表', 'details': str(e)}), 500

def api_get_yaml_content(file_path, file_name):
    """
    获取指定 YAML 文件的内容。
    :param file_path: 文件路径
    :param file_name: 文件名
    :return: YAML 文件内容的JSON响应
    """
    logger.info(f"收到获取 YAML 文件内容的请求，文件: {file_name}")
    
    try:
        if not file_path or not file_name:
            logger.warning("文件路径或文件名为空, 返回默认配置文件")
        
        # 获取指定 YAML 文件的内容
        content = get_yaml_file_content(file_path, file_name)
        
        if content is None:
            logger.error(f"无法读取文件: {file_name}")
            return jsonify({'error': f'无法读取文件: {file_name}'}), 404
        
        logger.info(f"成功获取文件 {file_name} 的内容")
        return jsonify({'content': content, 'code': 200})
    except Exception as e:
        logger.error(f"获取 YAML 文件内容失败: {str(e)}", exc_info=True)
        return jsonify({'error': '错误的获取 YAML 文件内容', 'details': str(e)}), 500
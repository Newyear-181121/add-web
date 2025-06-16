import logging
from flask import jsonify, request
from add_bookmark import load_bookmarks, add_bookmark, save_bookmarks

# 设置日志记录器
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

# api.py
from flask import jsonify, request
from models.add_bookmark import load_bookmarks, add_bookmark, save_bookmarks

def api_get_bookmarks():
    """
    处理获取书签的分组API 请求。
    :return: 书签数据的JSON响应
    """
    bookmarks = load_bookmarks()
    return jsonify(bookmarks)

def api_add_bookmark():
    """
    处理添加书签的 API 请求。
    :return: 操作结果的JSON响应
    """
    data = request.get_json()
    group_name = data.get('group_name')
    service_name = data.get('service_name')
    abbr = data.get('abbr')
    url = data.get('url')
    if group_name and service_name and url:
        add_bookmark(group_name, service_name, abbr, url)
        return jsonify({'message': 'Bookmark added successfully'})
    else:
        return jsonify({'error': 'Missing required fields'}), 400

def api_save_bookmarks():
    """
    处理保存书签的 API 请求。
    :return: 操作结果的JSON响应
    """
    data = request.get_json()
    save_bookmarks(data)
    return jsonify({'message': 'Bookmarks saved successfully'})

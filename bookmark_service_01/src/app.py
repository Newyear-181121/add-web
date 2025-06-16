from flask import Flask, render_template, request, jsonify
import logging
from api import api_get_bookmarks, api_add_bookmark, api_save_bookmarks, api_get_configs, api_get_yaml_content
from add_bookmark import get_bookmarks_groups

app = Flask(__name__)

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='[app] - %(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """
    渲染添加书签的页面。
    :return: 渲染后的HTML页面
    """
    try:
        groups = get_bookmarks_groups()
        logger.info("成功获取书签分组列表，共 %d 个分组", len(groups))
        return render_template('add_bookmark.html', groups=groups)
    except Exception as e:
        logger.error("获取书签分组列表失败: %s", str(e))
        return jsonify({"error": "获取书签分组失败"}), 500



@app.route('/api/bookmarks', methods=['GET'])
def get_bookmarks():
    """
    处理获取书签的API请求。
    :return: 书签数据的JSON响应
    """
    logger.info("收到获取书签数据的请求: %s", request.remote_addr)
    
    try:
        # 打印请求信息
        logger.debug("请求头: %s", request.headers)
        logger.debug("请求参数: %s", request.args)
        
        # 调用API处理函数
        response = api_get_bookmarks()
        
        # 打印响应信息
        logger.info("返回书签数据，状态码: 200")
        return response
    except Exception as e:
        logger.error("处理获取书签请求时发生错误: %s", str(e))
        return jsonify({"error": "获取书签数据失败"}), 500

@app.route('/api/bookmarks', methods=['POST'])
def add_bookmark():
    """
    处理添加书签的API请求。
    :return: 操作结果的JSON响应
    """
    logger.info("收到添加书签的请求: %s", request.remote_addr)
    
    try:
        # 打印请求信息
        logger.debug("请求头: %s", request.headers)
        logger.debug("请求体: %s", request.get_data(as_text=True))
        
        # 调用API处理函数
        response = api_add_bookmark()
        
        # 打印响应信息
        logger.info("添加书签成功，状态码: %s", response.status_code)
        return response
    except Exception as e:
        logger.error("处理添加书签请求时发生错误: %s", str(e))
        return jsonify({"error": "添加书签失败"}), 500

@app.route('/api/bookmarks/save', methods=['POST'])
def save_bookmarks():
    """
    处理保存书签的API请求。
    :return: 操作结果的JSON响应
    """
    logger.info("收到保存书签的请求: %s", request.remote_addr)
    
    try:
        # 打印请求信息
        logger.debug("请求头: %s", request.headers)
        logger.debug("请求体: %s", request.get_data(as_text=True))
        
        # 调用API处理函数
        response = api_save_bookmarks()
        
        # 打印响应信息
        logger.info("保存书签成功，状态码: %s", response.status_code)
        return response
    except Exception as e:
        logger.error("处理保存书签请求时发生错误: %s", str(e))
        return jsonify({"error": "保存书签失败"}), 500

@app.route('/api/config/files', methods=['GET'])
def get_configs():
    """
    处理获取配置文件的API请求。
    :return: 配置文件的JSON响应
    """
    logger.info("收到获取配置文件的请求: %s", request.remote_addr)
    
    try:
        dir = request.args.get('dir')
        logger.debug("请求参数: %s", request.args)
        
        # 调用API处理函数
        response = api_get_configs(dir)
        
        # 打印响应信息
        logger.info("获取配置文件成功，状态码: %s", response.status_code)
        return response
    except Exception as e:
        logger.error("处理获取配置文件请求时发生错误: %s", str(e))
        return jsonify({"error": "获取配置文件失败"}), 500

@app.route('/api/config/get_yaml_content', methods=['GET'])
def get_yaml_content():
    """
    处理获取YAML文件的内容API请求。
    :return: YAML文件的内容JSON响应
    """
    logger.info("收到获取YAML文件内容的请求: %s", request.remote_addr)
    
    try:
        file_path = request.args.get('file_path')
        file_name = request.args.get('file_name')
        logger.debug("请求参数: file_path=%s, file_name=%s", file_path, file_name)
        
        # 调用API处理函数
        response = api_get_yaml_content(file_path, file_name)
        
        # 打印响应信息
        logger.info("获取YAML文件内容成功，状态码: %s", response.status_code)
        return response
    except Exception as e:
        logger.error("处理获取YAML文件内容请求时发生错误: %s", str(e))
        return jsonify({"error": "获取YAML文件内容失败"}), 500
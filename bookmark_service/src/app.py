# main.py
import os
from flask import Flask, jsonify, render_template
from api import api_get_bookmarks, api_add_bookmark, api_save_bookmarks
from models.add_bookmark import get_bookmarks_groups
from models.config_manager import ConfigManager

app = Flask(__name__)

@app.route('/')
def index():
    """
    渲染添加书签的页面。
    :return: 渲染后的HTML页面
    """
    groups = get_bookmarks_groups()
    return render_template('templates/add_bookmark.html', groups=groups)
    # return render_template('config_manager.html', groups=groups)

@app.route('/api/bookmarks', methods=['GET'])
def get_bookmarks():
    """
    处理获取书签的API请求。
    :return: 书签数据的JSON响应
    """
    return api_get_bookmarks()

@app.route('/api/bookmarks', methods=['POST'])
def add_bookmark():
    """
    处理添加书签的API请求。
    :return: 操作结果的JSON响应
    """
    return api_add_bookmark()

@app.route('/api/bookmarks/save', methods=['POST'])
def save_bookmarks():
    """
    处理保存书签的API请求。
    :return: 操作结果的JSON响应
    """
    return api_save_bookmarks()


@app.route("/api/config/files", methods=['GET'])
async def api_get_config_files():
    """获取配置文件列表"""
    try:
        config_files = ConfigManager.get_config_files()
        return {"status": "success", "data": config_files}
    except Exception as e:
        raise  jsonify(status_code=500, detail=f"获取配置文件列表失败: {str(e)}")

@app.route("/api/config/active", methods=['GET'])
async def api_get_active_config():
    """获取当前活动配置"""
    try:
        active_config = ConfigManager.get_active_config()
        return {"status": "success", "data": active_config}
    except Exception as e:
        raise jsonify(status_code=500, detail=f"获取当前活动配置失败: {str(e)}")

@app.route("/api/config/switch", methods=['POST'])
async def api_switch_config(file_name: str):
    """切换配置文件"""
    try:
        success = ConfigManager.switch_config(file_name)
        if success:
            return {"status": "success", "message": f"已成功切换到配置: {file_name}"}
        else:
            raise jsonify(status_code=400, detail=f"配置文件 {file_name} 不存在")
    except Exception as e:
        raise jsonify(status_code=500, detail=f"切换配置文件失败: {str(e)}")

@app.route("/api/config/content", methods=['GET'])
async def api_get_config_content(file_name: str):
    """获取配置文件内容"""
    try:
        file_path = os.path.join(CONFIG_DIR, file_name)
        content = ConfigManager.get_config_content(file_path)
        
        if content is not None:
            return {"status": "success", "data": content}
        else:
            raise jsonify(status_code=404, detail=f"无法获取配置文件内容")
    except Exception as e:
        raise jsonify(status_code=500, detail=f"获取配置文件内容失败: {str(e)}")    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
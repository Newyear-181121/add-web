# main.py
from flask import Flask, render_template, request, send_from_directory
from api import api_get_bookmarks, api_add_bookmark, api_save_bookmarks
from add_bookmark import get_bookmarks_groups
import logging

# 声明 Flask 应用
app = Flask(__name__)

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """
    渲染添加书签的页面。
    :return: 渲染后的HTML页面
    """
    groups = get_bookmarks_groups()
    return render_template('add_bookmark.html', groups=groups)



@app.route('/api/bookmarks', methods=['GET'])
def get_bookmarks():
    """
    处理获取书签的API请求。
    :return: 书签数据的JSON响应
    """
    # 添加日志打印，
    # 以便在调试时查看请求是否到达
    print("请求书签数据！")
    return api_get_bookmarks()

@app.route('/api/bookmarks', methods=['POST'])
def add_bookmark():
    """
    处理添加书签的API请求。
    :return: 操作结果的JSON响应
    """
    data = request.get_json()
    print(f"/api/bookmarks -- 添加书签请求数据: {data}")
    return api_add_bookmark()

@app.route('/api/bookmarks/save', methods=['POST'])
def save_bookmarks():
    """
    处理保存书签的API请求。
    :return: 操作结果的JSON响应
    """
    return api_save_bookmarks()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
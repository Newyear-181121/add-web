### 配置文件管理页面设计方案

根据您的需求，我将设计一个配置文件管理页面，用于识别并切换不同的配置文件。以下是完整的伪代码逻辑和实现方案：

### 1. 新增配置文件管理页面的伪代码逻辑

#### 文件和目录结构
```
bookmark_service/
├── src
│   ├── main.py
│   ├── api.py
│   ├── add_bookmark.py
│   ├── config.py
│   ├── templates/
│   │   ├── add_bookmark.html
│   │   └── config_manager.html
├── Dockerfile
├── requirements.txt
├── docker-compose.yaml
```

#### 各文件功能说明

##### `config.py`
- **新增功能**：添加配置文件目录和目标配置文件路径
- **新增变量**：
  - `CONFIG_DIR`: 配置文件所在目录
  - `TARGET_CONFIG_PATH`: 目标配置文件路径

```python
# config.py
import os

BOOKMARK_CONFIG_PATH = os.path.join(os.getcwd(), 'bookmarks.yaml')
BOOKMARK_DIRS = os.path.dirname(BOOKMARK_CONFIG_PATH)

# 新增配置文件管理相关路径
CONFIG_DIR = os.path.dirname("/app/configs")  # 配置文件目录
TARGET_CONFIG_PATH = os.path.join(BOOKMARK_DIRS, "active_config.yaml")  # 目标配置文件路径
```

##### `add_bookmark.py`
- **新增功能**：配置文件管理相关函数
- **新增函数**：
  - `get_config_files()`: 获取配置目录下的所有文件
  - `switch_config(file_name)`: 切换到指定配置文件
  - `get_active_config()`: 获取当前活动配置文件

```python
# add_bookmark.py
import os
import yaml
import shutil
from config import BOOKMARK_CONFIG_PATH, CONFIG_DIR, TARGET_CONFIG_PATH

# 原有函数保持不变...

# 新增配置文件管理函数
def get_config_files():
    """获取配置目录下的所有配置文件"""
    try:
        files = os.listdir(CONFIG_DIR)
        # 过滤只保留.yaml和.yml文件
        return [f for f in files if f.endswith(('.yaml', '.yml'))]
    except Exception as e:
        print(f"Error listing config files: {e}")
        return []

def switch_config(file_name):
    """切换到指定配置文件"""
    source_path = os.path.join(CONFIG_DIR, file_name)
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Config file {file_name} not found")
    
    # 复制选中的配置文件到目标路径
    shutil.copy2(source_path, TARGET_CONFIG_PATH)
    return True

def get_active_config():
    """获取当前活动配置文件"""
    try:
        if os.path.exists(TARGET_CONFIG_PATH):
            return os.path.basename(TARGET_CONFIG_PATH)
        return None
    except Exception as e:
        print(f"Error getting active config: {e}")
        return None
```

##### `api.py`
- **新增API接口**：
  - `api_get_config_files()`: 获取配置文件列表
  - `api_switch_config()`: 切换配置文件
  - `api_get_active_config()`: 获取当前活动配置

```python
# api.py
from flask import jsonify, request
from add_bookmark import load_bookmarks, add_bookmark, save_bookmarks, get_config_files, switch_config, get_active_config

# 原有API函数保持不变...

# 新增配置文件管理API
@app.route('/api/config/files', methods=['GET'])
def api_get_config_files():
    """获取配置文件列表"""
    files = get_config_files()
    return jsonify(files)

@app.route('/api/config/switch', methods=['POST'])
def api_switch_config():
    """切换配置文件"""
    data = request.get_json()
    file_name = data.get('file_name')
    if not file_name:
        return jsonify({'error': 'Missing file_name'}), 400
    
    try:
        switch_config(file_name)
        return jsonify({'message': f'Successfully switched to {file_name}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/config/active', methods=['GET'])
def api_get_active_config():
    """获取当前活动配置"""
    active_config = get_active_config()
    return jsonify(active_config)
```

##### `main.py`
- **新增路由**：配置文件管理页面
```python
# main.py
from flask import Flask, render_template
from api import api_get_bookmarks, api_add_bookmark, api_save_bookmarks, api_get_config_files, api_switch_config, api_get_active_config
from add_bookmark import get_bookmarks_groups

app = Flask(__name__)

# 原有路由保持不变...

# 新增配置文件管理页面路由
@app.route('/config_manager')
def config_manager():
    """渲染配置文件管理页面"""
    config_files = get_config_files()
    active_config = get_active_config()
    return render_template('config_manager.html', config_files=config_files, active_config=active_config)

# 原有API路由保持不变...
```

##### `templates/config_manager.html`
- **页面功能**：
  - 显示配置文件下拉框
  - 切换配置文件
  - 显示当前活动配置
  - 提供配置文件管理操作

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Config Manager</title>
</head>
<body>
    <h1>配置文件管理</h1>
    
    <div id="config-selector">
        <label for="config-files">选择配置文件:</label>
        <select id="config-files">
            <option value="" disabled selected>请选择配置文件</option>
            <!-- 配置文件选项将通过JavaScript动态加载 -->
        </select>
        <button id="switch-btn">切换配置</button>
    </div>
    
    <div id="active-config" style="margin-top: 20px;">
        <h3>当前活动配置: <span id="current-config">加载中...</span></h3>
    </div>
    
    <div id="config-actions" style="margin-top: 20px;">
        <button id="reload-btn">重新加载配置</button>
        <button id="refresh-btn">刷新配置列表</button>
    </div>
    
    <div id="status-message" style="margin-top: 20px; color: green;"></div>
    
    <script>
        // 页面加载时初始化
        document.addEventListener('DOMContentLoaded', function() {
            loadConfigFiles();
            loadActiveConfig();
            
            // 绑定按钮事件
            document.getElementById('switch-btn').addEventListener('click', switchConfig);
            document.getElementById('refresh-btn').addEventListener('click', loadConfigFiles);
            document.getElementById('reload-btn').addEventListener('click', reloadConfig);
        });
        
        // 加载配置文件列表
        function loadConfigFiles() {
            fetch('/api/config/files')
                .then(response => response.json())
                .then(files => {
                    const configSelect = document.getElementById('config-files');
                    // 清空现有选项
                    while (configSelect.options.length > 1) {
                        configSelect.remove(1);
                    }
                    
                    // 添加新选项
                    files.forEach(file => {
                        const option = document.createElement('option');
                        option.value = file;
                        option.textContent = file;
                        configSelect.appendChild(option);
                    });
                    
                    // 更新状态
                    updateStatus(`已加载 ${files.length} 个配置文件`);
                })
                .catch(error => {
                    console.error('Error loading config files:', error);
                    updateStatus('加载配置文件失败', 'error');
                });
        }
        
        // 加载当前活动配置
        function loadActiveConfig() {
            fetch('/api/config/active')
                .then(response => response.json())
                .then(activeConfig => {
                    document.getElementById('current-config').textContent = activeConfig || '未选择配置';
                })
                .catch(error => {
                    console.error('Error loading active config:', error);
                    document.getElementById('current-config').textContent = '加载失败';
                });
        }
        
        // 切换配置文件
        function switchConfig() {
            const configSelect = document.getElementById('config-files');
            const selectedFile = configSelect.value;
            
            if (!selectedFile) {
                updateStatus('请先选择一个配置文件', 'error');
                return;
            }
            
            fetch('/api/config/switch', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ file_name: selectedFile })
            })
            .then(response => response.json())
            .then(result => {
                if (result.message) {
                    updateStatus(result.message);
                    loadActiveConfig();
                } else if (result.error) {
                    updateStatus(result.error, 'error');
                }
            })
            .catch(error => {
                console.error('Error switching config:', error);
                updateStatus('切换配置失败', 'error');
            });
        }
        
        // 重新加载配置
        function reloadConfig() {
            updateStatus('配置已重新加载');
            // 这里可以添加实际的重新加载逻辑
        }
        
        // 更新状态消息
        function updateStatus(message, type = 'success') {
            const statusElement = document.getElementById('status-message');
            statusElement.textContent = message;
            statusElement.style.color = type === 'error' ? 'red' : 'green';
            
            // 3秒后清除消息
            setTimeout(() => {
                statusElement.textContent = '';
            }, 3000);
        }
    </script>
</body>
</html>
```

### 2. 页面交互流程

1. 用户访问 `/config_manager` 页面
2. 页面加载时自动获取并显示配置文件列表和当前活动配置
3. 用户从下拉菜单选择配置文件
4. 点击"切换配置"按钮
5. 前端发送API请求到后端
6. 后端将选中的配置文件复制到目标位置
7. 页面刷新当前活动配置显示

### 3. 改进建议

1. **添加配置文件预览功能**：点击配置文件时显示其内容预览
2. **配置文件编辑功能**：允许直接在页面上编辑配置文件
3. **配置文件备份功能**：切换前自动备份当前配置
4. **配置文件上传功能**：支持上传新的配置文件
5. **配置文件版本控制**：记录配置变更历史

这个配置文件管理页面与之前的书签管理功能可以无缝集成，提供完整的配置管理解决方案。
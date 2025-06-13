新增加一个文件切换功能

以下是修改后的改动


### 1. 新增配置文件管理页面的伪代码逻辑

#### 文件和目录结构
```
bookmark_service/
├── src
│   ├── main.py
│   ├── api.py
│   ├── config.py
│   ├── templates/
│   │   ├── add_bookmark.html
│   │   └── config_manager.html   （新增文夹）
│   ├── model/   （新增文件夹）
│   │   ├── add_bookmark.py   （移动文夹）
│   │   └── config_manager.py  （新增文夹）
├── Dockerfile
├── requirements.txt
├── docker-compose.yaml
├── configs  （新增文件夹）
```

#### 各文件功能说明

##### `config.py`
- **新增功能**：添加配置文件目录和目标配置文件路径
- **新增变量**：
  - `CONFIG_DIR`: 配置文件所在目录
  - `TARGET_CONFIG_PATH`: 目标配置文件路径


##### `add_bookmark.py`
- **新增功能**：配置文件管理相关函数
- **新增函数**：
  - `get_config_files()`: 获取配置目录下的所有文件
  - `switch_config(file_name)`: 切换到指定配置文件
  - `get_active_config()`: 获取当前活动配置文件

  ##### `api.py`
- **新增API接口**：
  - `api_get_config_files()`: 获取配置文件列表
  - `api_switch_config()`: 切换配置文件
  - `api_get_active_config()`: 获取当前活动配置


##### `main.py`
- **新增路由**：配置文件管理页面

##### `templates/config_manager.html`
- **页面功能**：
  - 显示当前活动配置
  - 显示配置文件下拉框
  - 切换配置文件
  - 确定切换按钮


### 2. 页面交互流程

1. 默认访问  `/` 页面，打开`add_bookmarks.html`页面
2. 在 addbookmarks.html 页面下方引入/config_manager 页面
3. `/config_manager` 页面加载时自动获取并显示配置文件列表和当前活动配置
4. 用户从下拉菜单选择配置文件
5. 点击"切换配置"按钮
6. 前端发送API请求到后端
7. 后端将选中的配置文件复制到目标位置
8. 页面刷新当前活动配置显示

### 3. 改进建议
1. **配置文件版本控制**：记录配置变更历史，内容记录到日志文件中。



### 要求
符合以上伪代码的逻辑要求，输出详细的代码逻辑，并给出注释。
### 1. 书签配置文件相关格式

书签配置文件格式示例：

```yaml
- groups1:
    - bookmark1:
        - abbr: GH
          href: https://github.com/
- groups2:
    - bookmark2:
        - abbr: RE
          href: https://reddit.com/
- groups3:
    - bookmark3:
        - abbr: YT
          href: https://youtube.com/
- groups4:
    - test1:
        - abbr: ts
          href: https://youtube.com/
    - te:
        - abbr: tt
          href: https://youtube.com/
    - t2:
        - abbr: tt2
          href: https://youtube.com/
    - 项目列表:
        - abbr: tt
          href: https://youtube.com/
```


### 2. Python 服务伪代码逻辑

#### 文件和目录结构
```
bookmark_service/
├── src
│   ├── main.py
│   ├── api.py
│   ├── add_bookmark.py
│   ├── config.py
│   ├── templates/
│   │   └── add_bookmark.html
├── Dockerfile
├── requirements.txt
├── docker-compose.yaml
```


#### 各文件功能说明

##### `config.py`
- **功能**：配置文件，包含书签配置文件的路径等信息。
- **函数和变量**：
  - `BOOKMARK_CONFIG_PATH`：书签配置文件的路径。
  - `BOOKMARK_DIRS`:：书签配置文件所在目录。

##### `add_bookmark.py`
- **功能**：提供书签相关的接口。
  - `load_bookmarks()`：从配置文件中加载书签数据。
  - `get_bookmarks_gropus()`: 获取书签分组。
  - `get_bookmarks_services(group_name)`: 获取分组下的书签服务。
  - `get_bookmarks_service(group_name, service_name)`: 获取分组下的书签服务。
  - `save_bookmarks(bookmarks)`：将书签数据保存到配置文件中。
  - `add_bookmark(group_name, service_name, service_type, url, ping)`：添加新的书签。
  - `add_bookmark_groups()`：添加新的书签分组。

##### `api.py`
- **功能**：处理api请求。
- **函数和功能模块**：
  - `api_get_bookmarks()`: 处理获取书签的分组API 请求。
  - `api_add_bookmark()`：处理添加书签的 API 请求。
  - `api_save_bookmarks()`：处理保存书签的 API 请求。

##### `main.py`
- **功能**：处理主要逻辑，调用各个模块。

### 3. 单独的 Python 页面伪代码逻辑

#### `templates/add_bookmark.html`
- **功能**：提供一个页面，用于用户输入书签信息并提交。
- **页面样式**：
  - 简单的表单，包含以下输入字段：
    - 分组名（Group Name）
    - 书签名（bookmark Name）
    - 缩写名（abbr）（可选）
    - 链接名 (URL)
  - 提交按钮。

- 其他功能描述：
    - 分组名:
      - 表单可以直接输入不存在的分组，
      - 也可以下拉框选择已经存在的分组。

### 4. dockerfile
- **功能**：将项目打包成镜像。
```dockerFile
FROM python:3.12.4-alpine

# 设置Alpine镜像源为阿里云加速
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

# 设置工作目录
WORKDIR /app

# 安装编译工具和依赖库
RUN --mount=type=cache,target=./cache/apk \
    apk add --no-cache build-base yaml-dev

# 升级pip和setuptools
RUN --mount=type=cache,target=./cache/pip \ 
    pip install --no-cache-dir --upgrade pip setuptools

# 安装特定版本的Cython（先于PyYAML安装）
RUN --mount=type=cache,target=./cache/pip \ 
    pip install --no-cache-dir --only-binary=:all: PyYAML -i https://pypi.tuna.tsinghua.edu.cn/simple || \
    pip install --no-cache-dir Cython==3.0.0 PyYAML -i https://pypi.tuna.tsinghua.edu.cn/simple 


# 安装Python依赖
COPY requirements.txt .

RUN --mount=type=cache,target=./cache/pip \ 
    pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 5000

# 启动应用
CMD ["python", "app.py"]




# --mount=type=cache
# 这是 Docker BuildKit 的功能，用于在构建过程中创建可重用的缓存目录
# 这个缓存独立于容器，存储在宿主机的 Docker 缓存空间中
# 主要加速下载过程（例如从 PyPI 下载包）
# --no-cache-dir
# 这是 pip 的选项，禁用 pip 在容器内部的缓存
# 防止将下载的包存储在容器的文件系统中
# 主要用于减小镜像体积


# pip -i 指定镜像
# 清华大学镜像：https://pypi.tuna.tsinghua.edu.cn/simple
# 阿里云镜像：https://mirrors.aliyun.com/pypi/simple/
# 豆瓣镜像：https://pypi.douban.com/simple/

```

### 5. docker-compose.yaml
- **功能**：使用配置文件管理容器的启动，以及启动参数
```yaml
version: '3'

services:
  app-dev-manager:
    image: config-manager
    container_name: ny-config-manager-dev
    ports:
      - "5000:5000"
    volumes:
      - .:/app  # 将当前目录挂载到容器的/app目录
      - ./configs:/app/configs  # 挂载配置目录，支持多个文件
      - ./uploads:/app/uploads
    environment:
      - FLASK_DEBUG=1  # 启用Flask调试模式
    command: flask run --host=0.0.0.0 --port=5000  # 使用Flask开发服务器
```


### 要求
符合以上伪代码的逻辑要求，输出详细的代码逻辑，并给出注释。




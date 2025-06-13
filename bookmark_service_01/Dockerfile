FROM python:3.12.4-alpine

# 设置Alpine镜像源为阿里云加速
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY requirements.txt .
COPY ./src .

# 安装编译工具和依赖库
RUN --mount=type=cache,target=~/.cache/apk \
    apk add --no-cache build-base yaml-dev

# 升级pip和setuptools
RUN --mount=type=cache,target=~/.cache/pip \ 
    pip install --no-cache-dir --upgrade pip setuptools

# 安装特定版本的Cython（先于PyYAML安装）
RUN --mount=type=cache,target=~/.cache/pip \ 
    pip install --no-cache-dir --only-binary=:all: PyYAML -i https://pypi.tuna.tsinghua.edu.cn/simple || \
    pip install --no-cache-dir Cython==3.0.0 PyYAML -i https://pypi.tuna.tsinghua.edu.cn/simple 


RUN --mount=type=cache,target=~/.cache/pip \ 
    pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple



# 暴露端口
EXPOSE 5000

# 启动应用
CMD ["python", "app.py"]


# docker build -t add_bookmark:latest .


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

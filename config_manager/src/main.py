import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api import router as api_router

# 创建FastAPI应用
app = FastAPI(title="书签服务配置管理系统", description="管理和切换不同的配置文件")

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 模板引擎配置
templates = Jinja2Templates(directory="templates")

# 注册API路由
app.include_router(api_router)

# 首页路由 - 书签添加页面
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("config_manager.html", {"request": request})

# 配置管理页面路由
@app.get("/add", response_class=HTMLResponse)
async def config_manager(request: Request):
    return templates.TemplateResponse("add_bookmark.html", {"request": request})

# 确保配置目录存在
@app.on_event("startup")
async def startup_event():
    config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "configs")
    os.makedirs(config_dir, exist_ok=True)    
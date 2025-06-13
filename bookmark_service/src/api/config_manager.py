from fastapi import APIRouter, HTTPException
from models.config_manager import ConfigManager

router = APIRouter()

@router.get("/api/config/files", tags=["配置管理"])
async def api_get_config_files():
    """获取配置文件列表"""
    try:
        config_files = ConfigManager.get_config_files()
        return {"status": "success", "data": config_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取配置文件列表失败: {str(e)}")

@router.get("/api/config/active", tags=["配置管理"])
async def api_get_active_config():
    """获取当前活动配置"""
    try:
        active_config = ConfigManager.get_active_config()
        return {"status": "success", "data": active_config}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取当前活动配置失败: {str(e)}")

@router.post("/api/config/switch", tags=["配置管理"])
async def api_switch_config(file_name: str):
    """切换配置文件"""
    try:
        success = ConfigManager.switch_config(file_name)
        if success:
            return {"status": "success", "message": f"已成功切换到配置: {file_name}"}
        else:
            raise HTTPException(status_code=400, detail=f"配置文件 {file_name} 不存在")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"切换配置文件失败: {str(e)}")

@router.get("/api/config/content", tags=["配置管理"])
async def api_get_config_content(file_name: str):
    """获取配置文件内容"""
    try:
        file_path = os.path.join(CONFIG_DIR, file_name)
        content = ConfigManager.get_config_content(file_path)
        
        if content is not None:
            return {"status": "success", "data": content}
        else:
            raise HTTPException(status_code=404, detail=f"无法获取配置文件内容")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取配置文件内容失败: {str(e)}")    
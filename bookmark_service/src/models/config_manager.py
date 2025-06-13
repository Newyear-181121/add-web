import os
import shutil
import json
from datetime import datetime
from typing import List, Dict, Optional
from config import CONFIG_DIR, TARGET_CONFIG_PATH

class ConfigManager:
    """配置文件管理类，负责配置文件的读取、切换和管理"""
    
    @staticmethod
    def get_config_files() -> List[Dict]:
        """获取配置目录下的所有配置文件信息
        
        Returns:
            配置文件列表，每个文件包含名称、大小、修改时间等信息
        """
        config_files = []
        
        # 检查配置目录是否存在
        if not os.path.exists(CONFIG_DIR):
            return config_files
            
        # 遍历配置目录下的所有文件
        for filename in os.listdir(CONFIG_DIR):
            file_path = os.path.join(CONFIG_DIR, filename)
            
            # 只处理文件，不处理目录
            if os.path.isfile(file_path) and filename.endswith(('.json', '.yaml', '.yml')):
                # 获取文件信息
                file_stat = os.stat(file_path)
                
                # 构建文件信息字典
                file_info = {
                    "name": filename,
                    "size": ConfigManager._format_size(file_stat.st_size),
                    "modified": datetime.fromtimestamp(file_stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                    "path": file_path
                }
                
                config_files.append(file_info)
        
        # 按修改时间排序，最新的文件排在前面
        config_files.sort(key=lambda x: x["modified"], reverse=True)
        
        return config_files
    
    @staticmethod
    def get_active_config() -> Optional[Dict]:
        """获取当前活动配置文件信息
        
        Returns:
            当前活动配置文件信息，如果不存在则返回None
        """
        if os.path.exists(TARGET_CONFIG_PATH):
            try:
                file_stat = os.stat(TARGET_CONFIG_PATH)
                return {
                    "name": os.path.basename(TARGET_CONFIG_PATH),
                    "size": ConfigManager._format_size(file_stat.st_size),
                    "modified": datetime.fromtimestamp(file_stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                    "path": TARGET_CONFIG_PATH
                }
            except Exception as e:
                print(f"获取活动配置文件信息失败: {e}")
                return None
        return None
    
    @staticmethod
    def switch_config(file_name: str) -> bool:
        """切换到指定的配置文件
        
        Args:
            file_name: 要切换的配置文件名称
            
        Returns:
            切换成功返回True，失败返回False
        """
        source_path = os.path.join(CONFIG_DIR, file_name)
        
        # 检查源文件是否存在
        if not os.path.exists(source_path):
            return False
            
        try:
            # 复制指定配置文件到目标位置
            shutil.copy2(source_path, TARGET_CONFIG_PATH)
            
            # 记录配置变更日志
            ConfigManager._log_config_change(file_name)
            
            return True
        except Exception as e:
            print(f"切换配置文件失败: {e}")
            return False
    
    @staticmethod
    def get_config_content(file_path: str) -> Optional[str]:
        """获取配置文件内容
        
        Args:
            file_path: 配置文件路径
            
        Returns:
            配置文件内容，如果读取失败则返回None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # 如果是JSON文件，格式化后返回
                if file_path.endswith('.json'):
                    content = json.load(f)
                    return json.dumps(content, indent=2, ensure_ascii=False)
                # 其他类型文件直接返回原始内容
                else:
                    return f.read()
        except Exception as e:
            print(f"读取配置文件内容失败: {e}")
            return None
    
    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """格式化文件大小
        
        Args:
            size_bytes: 文件大小（字节）
            
        Returns:
            格式化后的文件大小字符串
        """
        units = ['B', 'KB', 'MB', 'GB']
        unit_index = 0
        
        while size_bytes >= 1024 and unit_index < len(units) - 1:
            size_bytes /= 1024
            unit_index += 1
            
        return f"{size_bytes:.1f} {units[unit_index]}"
    
    @staticmethod
    def _log_config_change(file_name: str) -> None:
        """记录配置变更日志
        
        Args:
            file_name: 变更的配置文件名称
        """
        log_file = os.path.join(CONFIG_DIR, "config_changes.log")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"{timestamp} - 切换到配置: {file_name}\n")
        except Exception as e:
            print(f"记录配置变更日志失败: {e}")    
from typing import Dict, Any
from pathlib import Path
from ..generators.project_generator import ProjectGenerator

class ProjectTools:
    def __init__(self, knowledge_manager, memory_manager):
        self.knowledge_manager = knowledge_manager
        self.memory_manager = memory_manager
        # 使用默认路径初始化项目生成器
        self.project_generator = ProjectGenerator("./knowledge_base", "./memory/memory.db")

    async def create_project(self, 
                           project_name: str,
                           mcu_family: str,
                           toolchain: str = "gcc-arm-none-eabi") -> Dict[str, Any]:
        """创建新的FreeRTOS项目"""
        
        # 验证MCU支持
        if not self.knowledge_manager.validate_mcu_support(mcu_family):
            return {"error": f"MCU family {mcu_family} not supported"}
        
        # 生成项目结构
        project_structure = self.project_generator.generate_project(
            project_name, mcu_family, "./projects")
        
        # 记录到记忆库
        self.memory_manager.record_project_creation(
            project_name, mcu_family, toolchain)
        
        return {
            "status": "success",
            "project_name": project_name,
            "mcu_family": mcu_family,
            "files_created": project_structure,
            "next_steps": [
                "Configure project settings in config/",
                "Add tasks using generate_task tool",
                "Build project with make"
            ]
        }
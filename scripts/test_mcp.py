#!/usr/bin/env python3
"""MCP服务器测试脚本"""

import sys
import os
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from embedded_freertos_mcp.knowledge.knowledge_loader import KnowledgeLoader
from embedded_freertos_mcp.memory.memory_manager import MemoryManager
from embedded_freertos_mcp.generators.project_generator import ProjectGenerator

def test_knowledge_loader():
    """测试知识库加载器"""
    print("测试知识库加载器...")
    loader = KnowledgeLoader("./knowledge_base")
    
    # 测试可用芯片
    chips = loader.get_available_chips()
    print(f"可用芯片: {chips}")
    
    # 测试BK7252配置
    bk_config = loader.load_chip_config("bk7252")
    if bk_config:
        print(f"BK7252配置加载成功")
        print(f"芯片名称: {bk_config['chip']['name']}")
        print(f"核心: {bk_config['chip']['core']}")
        print(f"频率: {bk_config['chip']['frequency']}")
    else:
        print("BK7252配置加载失败")
    
    # 测试需求文档
    requirements = loader.load_requirements()
    if requirements:
        print("需求文档加载成功")
    else:
        print("需求文档加载失败")

def test_memory_manager():
    """测试记忆库管理器"""
    print("\n测试记忆库管理器...")
    memory = MemoryManager("./memory/test_memory.db")
    
    # 测试保存项目配置
    test_config = {
        "project_name": "test_project",
        "chip_family": "bk7252",
        "files": ["main.c", "Makefile"]
    }
    
    success = memory.save_project_config("test_project", "bk7252", test_config)
    if success:
        print("项目配置保存成功")
    else:
        print("项目配置保存失败")
    
    # 测试加载项目配置
    loaded_config = memory.load_project_config("test_project")
    if loaded_config:
        print("项目配置加载成功")
        print(f"项目名称: {loaded_config.get('project_name')}")
    else:
        print("项目配置加载失败")

def test_project_generator():
    """测试项目生成器"""
    print("\n测试项目生成器...")
    generator = ProjectGenerator("./knowledge_base", "./memory/test_memory.db")
    
    # 测试项目生成
    result = generator.generate_project("test_bk7252", "bk7252", "./test_output")
    
    if result["success"]:
        print("项目生成成功!")
        print(f"输出目录: {result['project_path']}")
        print(f"生成文件数: {len(result['generated_files'])}")
        print("前10个文件:")
        for file in result['generated_files'][:10]:
            print(f"  - {file}")
    else:
        print(f"项目生成失败: {result.get('error', '未知错误')}")

def main():
    """主测试函数"""
    print("嵌入式FreeRTOS MCP扩展测试")
    print("=" * 50)
    
    try:
        test_knowledge_loader()
        test_memory_manager()
        test_project_generator()
        
        print("\n" + "=" * 50)
        print("测试完成!")
        print("\n使用说明:")
        print("1. 安装依赖: pip install -r requirements.txt")
        print("2. 启动服务器: python scripts/start_server.py")
        print("3. 在文心快码中配置MCP服务器")
        print("4. 使用工具创建嵌入式FreeRTOS项目")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
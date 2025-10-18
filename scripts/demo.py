#!/usr/bin/env python3
"""嵌入式FreeRTOS MCP扩展演示脚本"""

import sys
import os
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from embedded_freertos_mcp.knowledge.knowledge_loader import KnowledgeLoader
from embedded_freertos_mcp.generators.project_generator import ProjectGenerator

def demo_bk7252_project():
    """演示BK7252项目生成"""
    print("=" * 60)
    print("嵌入式FreeRTOS MCP扩展演示")
    print("=" * 60)
    
    print("1. 初始化知识库加载器...")
    loader = KnowledgeLoader("./knowledge_base")
    
    print("2. 获取可用芯片列表...")
    chips = loader.get_available_chips()
    print(f"   支持的芯片: {', '.join(chips)}")
    
    print("3. 加载BK7252芯片信息...")
    bk_config = loader.load_chip_config("bk7252")
    if bk_config:
        chip_info = bk_config['chip']
        print(f"   芯片名称: {chip_info['name']}")
        print(f"   核心架构: {chip_info['core']}")
        print(f"   工作频率: {chip_info['frequency']}")
        print(f"   Flash大小: {chip_info['flash_size']}")
        print(f"   RAM大小: {chip_info['ram_size']}")
        
        print("4. 查看外设资源...")
        peripherals = bk_config['peripherals']
        for periph, details in peripherals.items():
            print(f"   {periph.upper()}: {details}")
    
    print("5. 生成BK7252 FreeRTOS项目...")
    generator = ProjectGenerator("./knowledge_base", "./memory/demo_memory.db")
    
    result = generator.generate_project(
        project_name="demo_bk7252_project",
        chip_family="bk7252",
        output_dir="./demo_output"
    )
    
    if result["success"]:
        print("   项目生成成功!")
        print(f"   输出目录: {result['project_path']}")
        print(f"   生成文件数: {len(result['generated_files'])}")
        
        print("6. 查看生成的关键文件:")
        key_files = [f for f in result['generated_files'] if any(ext in f for ext in ['.c', '.h', 'Makefile', '.ld'])]
        for file in key_files[:8]:  # 显示前8个关键文件
            print(f"   - {file}")
        
        print("\n7. 项目结构说明:")
        print("   src/          - 源代码目录")
        print("     main.c      - 主程序文件")
        print("     system.c    - 系统初始化")
        print("     tasks/      - FreeRTOS任务")
        print("   inc/          - 头文件目录")
        print("   drivers/      - 外设驱动")
        print("   freertos/     - FreeRTOS内核")
        print("   Makefile      - 构建脚本")
        print("   linker_script.ld - 链接脚本")
        
    else:
        print(f"   项目生成失败: {result.get('error', '未知错误')}")
    
    print("\n" + "=" * 60)
    print("演示完成!")
    print("\n下一步操作:")
    print("1. 进入项目目录: cd demo_output/demo_bk7252_project")
    print("2. 编译项目: make")
    print("3. 烧录到BK7252开发板")
    print("4. 使用文心快码继续开发")

def demo_usage_scenario():
    """演示使用场景"""
    print("\n" + "=" * 60)
    print("使用场景演示")
    print("=" * 60)
    
    print("场景: 使用文心快码创建BK7252 FreeRTOS项目")
    print("\n用户输入:")
    print('创建嵌入式FreeRTOS项目')
    print('- 项目名称: my_smart_device')
    print('- 芯片系列: bk7252')
    print('- 输出目录: ./projects')
    
    print("\nMCP扩展执行流程:")
    print("1. 读取BK7252芯片知识库")
    print("2. 分析项目需求文档")
    print("3. 生成完整的项目结构")
    print("4. 配置FreeRTOS内核参数")
    print("5. 生成外设驱动模板")
    print("6. 创建构建系统")
    print("7. 保存项目配置到记忆库")
    
    print("\n生成的项目包含:")
    print("- WiFi连接管理任务")
    print("- BLE通信任务")
    print("- 系统监控任务")
    print("- GPIO控制驱动")
    print("- UART调试输出")
    print("- 完整的Makefile构建系统")
    
    print("\n优势:")
    print("- 自动读取芯片规格书，避免手动配置错误")
    print("- 基于最佳实践的代码模板")
    print("- 记忆库保存项目配置，支持持续开发")
    print("- 与文心快码无缝集成，智能代码补全")

if __name__ == "__main__":
    demo_bk7252_project()
    demo_usage_scenario()
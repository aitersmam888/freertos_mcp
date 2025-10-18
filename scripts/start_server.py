#!/usr/bin/env python3
"""嵌入式FreeRTOS MCP服务器启动脚本"""

import sys
import os
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from embedded_freertos_mcp.server import FreeRTOSMCPServer
import asyncio

async def main():
    """主函数"""
    print("启动嵌入式FreeRTOS MCP服务器...")
    print("服务器名称: embedded-freertos-mcp")
    print("版本: 1.0.0")
    print("支持的芯片: BK7252, STM32F4, ESP32")
    print("=" * 50)
    
    try:
        server = FreeRTOSMCPServer()
        await server.start()
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"服务器启动失败: {e}")

if __name__ == "__main__":
    asyncio.run(main())
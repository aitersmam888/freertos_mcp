#!/usr/bin/env python3
"""MCP服务器主入口点"""

import asyncio
import logging
from .server import FreeRTOSMCPServer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """主函数"""
    server = FreeRTOSMCPServer()
    await server.start()

if __name__ == "__main__":
    asyncio.run(main())
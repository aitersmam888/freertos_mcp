#!/usr/bin/env python3
"""Main entry point for the Embedded FreeRTOS MCP Server."""

import asyncio
import logging
from .server import FreeRTOSMCPServer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Main async function to start the MCP server."""
    server = FreeRTOSMCPServer()
    await server.start()

if __name__ == "__main__":
    asyncio.run(main())
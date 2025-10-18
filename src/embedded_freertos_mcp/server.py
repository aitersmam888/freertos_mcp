#!/usr/bin/env python3
"""MCP服务器主文件 - 文心快码嵌入式FreeRTOS扩展"""

import asyncio
import logging
from typing import Any, Dict, List, Optional
try:
    from mcp.server import Server
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    import mcp.types as types
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    # 创建模拟类用于开发测试
    class Server:
        def __init__(self, name): pass
        def list_tools(self): 
            def decorator(func): return func
            return decorator
        def call_tool(self): 
            def decorator(func): return func
            return decorator
        def get_capabilities(self, **kwargs): return {}
        def run(self, *args, **kwargs): pass
    class types:
        Tool = type('Tool', (), {})
        TextContent = type('TextContent', (), {})
    class InitializationOptions: pass

from .knowledge.knowledge_loader import KnowledgeLoader
from .memory.memory_manager import MemoryManager
from .generators.project_generator import ProjectGenerator

logger = logging.getLogger(__name__)

class FreeRTOSMCPServer:
    """嵌入式FreeRTOS MCP服务器"""
    
    def __init__(self):
        self.server = Server("embedded-freertos-mcp")
        self.knowledge_loader: Optional[KnowledgeLoader] = None
        self.memory_manager: Optional[MemoryManager] = None
        self.project_generator: Optional[ProjectGenerator] = None
        
        # 注册工具处理函数
        self.server.list_tools()(self._list_tools)
        self.server.call_tool()(self._call_tool)
    
    async def start(self):
        """启动MCP服务器"""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="embedded-freertos-mcp",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities=None
                    )
                )
            )
    
    def _initialize_components(self, config: Dict[str, Any]):
        """初始化组件"""
        knowledge_base_path = config.get("knowledge_base_path", "./knowledge_base")
        memory_db_path = config.get("memory_db_path", "./memory/memory.db")
        
        self.knowledge_loader = KnowledgeLoader(knowledge_base_path)
        self.memory_manager = MemoryManager(memory_db_path)
        self.project_generator = ProjectGenerator(knowledge_base_path, memory_db_path)
    
    async def _list_tools(self) -> List[types.Tool]:
        """列出可用工具"""
        return [
            types.Tool(
                name="create_embedded_project",
                description="创建完整的嵌入式FreeRTOS项目，自动读取芯片知识库",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_name": {
                            "type": "string",
                            "description": "项目名称"
                        },
                        "chip_family": {
                            "type": "string", 
                            "description": "芯片系列（如：bk7252, stm32f4）",
                            "enum": self._get_available_chips()
                        },
                        "output_dir": {
                            "type": "string",
                            "description": "输出目录路径",
                            "default": "./projects"
                        }
                    },
                    "required": ["project_name", "chip_family"]
                }
            ),
            types.Tool(
                name="get_chip_info",
                description="获取芯片详细信息",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "chip_family": {
                            "type": "string",
                            "description": "芯片系列",
                            "enum": self._get_available_chips()
                        }
                    },
                    "required": ["chip_family"]
                }
            ),
            types.Tool(
                name="search_knowledge_base",
                description="搜索芯片规格书和文档",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "chip_family": {
                            "type": "string",
                            "description": "芯片系列",
                            "enum": self._get_available_chips()
                        },
                        "search_query": {
                            "type": "string",
                            "description": "搜索关键词"
                        }
                    },
                    "required": ["chip_family", "search_query"]
                }
            ),
            types.Tool(
                name="generate_driver_code",
                description="生成外设驱动代码",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "chip_family": {
                            "type": "string",
                            "description": "芯片系列",
                            "enum": self._get_available_chips()
                        },
                        "peripheral": {
                            "type": "string",
                            "description": "外设类型",
                            "enum": ["gpio", "uart", "spi", "i2c", "adc", "pwm"]
                        }
                    },
                    "required": ["chip_family", "peripheral"]
                }
            ),
            types.Tool(
                name="save_project_memory",
                description="保存项目配置到记忆库",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_name": {
                            "type": "string",
                            "description": "项目名称"
                        },
                        "chip_family": {
                            "type": "string",
                            "description": "芯片系列"
                        },
                        "config_data": {
                            "type": "object",
                            "description": "配置数据"
                        }
                    },
                    "required": ["project_name", "chip_family", "config_data"]
                }
            ),
            types.Tool(
                name="load_project_memory",
                description="从记忆库加载项目配置",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_name": {
                            "type": "string",
                            "description": "项目名称"
                        }
                    },
                    "required": ["project_name"]
                }
            )
        ]
    
    def _get_available_chips(self) -> List[str]:
        """获取可用芯片列表"""
        if self.knowledge_loader:
            return self.knowledge_loader.get_available_chips()
        return ["bk7252", "stm32f4", "esp32"]
    
    async def _call_tool(self, name: str, arguments: Dict[str, Any]) -> List[Any]:
        """调用工具"""
        try:
            if not self.knowledge_loader:
                # 使用默认配置初始化
                self._initialize_components({})
            
            if name == "create_embedded_project":
                return await self._create_project(arguments)
            elif name == "get_chip_info":
                return await self._get_chip_info(arguments)
            elif name == "search_knowledge_base":
                return await self._search_knowledge_base(arguments)
            elif name == "generate_driver_code":
                return await self._generate_driver_code(arguments)
            elif name == "save_project_memory":
                return await self._save_project_memory(arguments)
            elif name == "load_project_memory":
                return await self._load_project_memory(arguments)
            else:
                raise ValueError(f"未知工具: {name}")
                
        except Exception as e:
            logger.error(f"工具调用失败: {e}")
            if MCP_AVAILABLE:
                return [types.TextContent(
                    type="text",
                    text=f"错误: {str(e)}"
                )]
            else:
                return [{"type": "text", "text": f"错误: {str(e)}"}]
    
    async def _create_project(self, arguments: Dict[str, Any]) -> List[Any]:
        """创建项目工具"""
        project_name = arguments["project_name"]
        chip_family = arguments["chip_family"]
        output_dir = arguments.get("output_dir", "./projects")
        
        if not self.project_generator:
            raise RuntimeError("项目生成器未初始化")
        
        result = self.project_generator.generate_project(project_name, chip_family, output_dir)
        
        if result["success"]:
            text = f"""项目创建成功！

项目名称: {project_name}
芯片型号: {chip_family}
输出目录: {result['project_path']}

生成的文件:
{chr(10).join(f"- {file}" for file in result['generated_files'][:10])}
... 共 {len(result['generated_files'])} 个文件

芯片信息:
- 核心: {result['chip_info']['chip']['core']}
- 频率: {result['chip_info']['chip']['frequency']}
- Flash: {result['chip_info']['chip']['flash_size']}
- RAM: {result['chip_info']['chip']['ram_size']}

项目已保存到记忆库，可以使用 load_project_memory 工具重新加载。"""
        else:
            text = f"项目创建失败: {result['error']}"
        
        if MCP_AVAILABLE:
            return [types.TextContent(type="text", text=text)]
        else:
            return [{"type": "text", "text": text}]
    
    async def _get_chip_info(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """获取芯片信息工具"""
        chip_family = arguments["chip_family"]
        
        chip_config = self.knowledge_loader.load_chip_config(chip_family)
        datasheet_info = self.knowledge_loader.load_datasheet_info(chip_family)
        sdk_info = self.knowledge_loader.load_sdk_info(chip_family)
        
        if not chip_config:
            return [types.TextContent(type="text", text=f"未找到芯片 {chip_family} 的信息")]
        
        text = f"""芯片信息: {chip_config['chip']['name']}

基本参数:
- 系列: {chip_config['chip']['family']}
- 核心: {chip_config['chip']['core']}
- 频率: {chip_config['chip']['frequency']}
- Flash: {chip_config['chip']['flash_size']}
- RAM: {chip_config['chip']['ram_size']}

外设资源:
{chr(10).join(f"- {periph}: {details}" for periph, details in chip_config['peripherals'].items())}

内存映射:
- Flash: {chip_config['memory_map']['flash_start']} - {chip_config['memory_map']['flash_end']}
- RAM: {chip_config['memory_map']['ram_start']} - {chip_config['memory_map']['ram_end']}

编译配置:
工具链: {chip_config['compiler']['toolchain']}
编译选项: {', '.join(chip_config['compiler']['flags'][:3])}..."""

        if datasheet_info:
            text += f"\n\n规格书: {', '.join(datasheet_info['datasheet_files'])}"
        
        if sdk_info:
            text += f"\n\nSDK驱动: {', '.join(sdk_info['available_drivers'][:5])}..."
        
        return [types.TextContent(type="text", text=text)]
    
    async def _search_knowledge_base(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """搜索知识库工具"""
        chip_family = arguments["chip_family"]
        search_query = arguments["search_query"]
        
        # 这里可以实现更复杂的搜索逻辑
        chip_config = self.knowledge_loader.load_chip_config(chip_family)
        
        if not chip_config:
            return [types.TextContent(type="text", text=f"未找到芯片 {chip_family} 的信息")]
        
        # 简单的关键词匹配搜索
        results = []
        search_lower = search_query.lower()
        
        # 搜索芯片配置
        chip_text = f"{chip_config['chip']['name']} {chip_config['chip']['description']}".lower()
        if search_lower in chip_text:
            results.append("芯片基本信息")
        
        # 搜索外设
        for periph, details in chip_config['peripherals'].items():
            if search_lower in periph.lower():
                results.append(f"外设: {periph} - {details}")
        
        if results:
            text = f"搜索 '{search_query}' 在 {chip_family} 中的结果:\n\n" + "\n".join(f"- {result}" for result in results[:10])
        else:
            text = f"未找到与 '{search_query}' 相关的内容"
        
        return [types.TextContent(type="text", text=text)]
    
    async def _generate_driver_code(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """生成驱动代码工具"""
        chip_family = arguments["chip_family"]
        peripheral = arguments["peripheral"]
        
        chip_config = self.knowledge_loader.load_chip_config(chip_family)
        if not chip_config:
            return [types.TextContent(type="text", text=f"未找到芯片 {chip_family} 的信息")]
        
        # 生成简单的驱动代码模板
        driver_code = self._generate_driver_template(chip_family, peripheral, chip_config)
        
        return [types.TextContent(type="text", text=driver_code)]
    
    def _generate_driver_template(self, chip_family: str, peripheral: str, chip_config: Dict[str, Any]) -> str:
        """生成驱动代码模板"""
        if peripheral == "gpio":
            return f"""// {chip_config['chip']['name']} GPIO驱动模板
#include "gpio.h"

void GPIO_Init(GPIO_TypeDef *GPIOx, GPIO_InitTypeDef *init)
{{
    // GPIO初始化代码
    // 芯片: {chip_family}
    // 支持 {chip_config['peripherals']['gpio']['ports']} 端口
}}

void GPIO_WritePin(GPIO_TypeDef *GPIOx, uint16_t pin, GPIO_PinState state)
{{
    // 写GPIO引脚
}}

GPIO_PinState GPIO_ReadPin(GPIO_TypeDef *GPIOx, uint16_t pin)
{{
    // 读GPIO引脚
    return GPIO_PIN_RESET;
}}"""
        
        elif peripheral == "uart":
            return f"""// {chip_config['chip']['name']} UART驱动模板
#include "uart.h"

void UART_Init(UART_TypeDef *UARTx, UART_InitTypeDef *init)
{{
    // UART初始化
    // 波特率范围: {chip_config['peripherals']['uart']['baud_rate']}
    // 支持 {chip_config['peripherals']['uart']['count']} 个UART接口
}}

void UART_SendData(UART_TypeDef *UARTx, uint8_t data)
{{
    // 发送数据
}}

uint8_t UART_ReceiveData(UART_TypeDef *UARTx)
{{
    // 接收数据
    return 0;
}}"""
        
        else:
            return f"// {chip_config['chip']['name']} {peripheral.upper()} 驱动模板\n// 驱动代码生成功能待完善"
    
    async def _save_project_memory(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """保存项目记忆工具"""
        project_name = arguments["project_name"]
        chip_family = arguments["chip_family"]
        config_data = arguments["config_data"]
        
        success = self.memory_manager.save_project_config(project_name, chip_family, config_data)
        
        if success:
            text = f"项目 '{project_name}' 配置已保存到记忆库"
        else:
            text = f"保存项目配置失败"
        
        return [types.TextContent(type="text", text=text)]
    
    async def _load_project_memory(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """加载项目记忆工具"""
        project_name = arguments["project_name"]
        
        config = self.memory_manager.load_project_config(project_name)
        
        if config:
            text = f"""项目 '{project_name}' 配置:

芯片: {config.get('chip_family', '未知')}
生成文件数: {len(config.get('generated_files', []))}

配置详情已加载，可以使用相关工具继续开发。"""
        else:
            text = f"未找到项目 '{project_name}' 的配置"
        
        return [types.TextContent(type="text", text=text)]
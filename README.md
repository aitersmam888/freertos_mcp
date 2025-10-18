# 文心快码嵌入式FreeRTOS MCP扩展

专为文心快码设计的嵌入式FreeRTOS开发MCP扩展，支持BK7252等芯片的自动项目生成。提供完整的嵌入式开发工作流，从项目创建到代码生成的一站式解决方案。

## 🚀 功能特性

### 核心功能
- **智能项目生成**: 根据芯片知识库自动创建完整的FreeRTOS项目结构
- **知识库集成**: 集成芯片规格书、SDK文档和项目需求文档
- **记忆库功能**: SQLite数据库保存项目配置，支持持续开发
- **多芯片支持**: 支持BK7252、STM32F4、ESP32等主流嵌入式芯片
- **模板系统**: 基于Jinja2的智能代码模板生成

### 增强功能
- **代码验证**: 自动验证生成的代码符合FreeRTOS最佳实践
- **外设驱动生成**: 自动生成GPIO、UART、SPI、I2C等外设驱动代码
- **内存分析**: 堆栈使用分析和优化建议
- **项目配置管理**: YAML配置文件管理芯片特性和项目设置

## 📋 系统要求

### 基础环境
- **操作系统**: Windows 10/11, Linux, macOS
- **Python**: 3.8 或更高版本
- **包管理器**: pip 最新版本

### 开发工具（可选）
- **MSYS2** (Windows): 用于GCC ARM工具链
- **GCC ARM工具链**: 用于代码编译
- **文心快码插件**: 用于MCP集成

## 🔧 安装部署

### 1. 快速安装

```bash
# 克隆项目
git clone https://github.com/aitersmam888/freertos_mcp.git
cd embedded_freertos_mcp

# 安装Python依赖
pip install -r requirements.txt

# 安装开发依赖（可选）
pip install -r requirements-dev.txt
```

### 2. 开发环境配置

#### Windows环境
```bash
# 安装MSYS2（如果尚未安装）
# 下载地址: https://www.msys2.org/

# 在MSYS2中安装GCC ARM工具链
pacman -S mingw-w64-x86_64-arm-none-eabi-gcc
pacman -S make
```

#### Linux环境
```bash
# Ubuntu/Debian
sudo apt-get install gcc-arm-none-eabi make

# CentOS/RHEL
sudo yum install arm-none-eabi-gcc make
```

#### macOS环境
```bash
# 使用Homebrew安装
brew install arm-none-eabi-gcc make
```

### 3. 文心快码集成配置

在文心快码设置中添加MCP服务器配置：

```json
{
  "mcpServers": {
    "embedded-freertos": {
      "command": "python",
      "args": ["-m", "src.embedded_freertos_mcp"]
    }
  }
}
```

### 4. 环境验证

运行测试命令验证安装：

```bash
# 验证Python模块导入
python -c "from src.embedded_freertos_mcp.models.chip_analysis import ChipCapabilities; print('✅ 模型导入成功')"

# 验证知识库加载
python -c "from src.embedded_freertos_mcp.knowledge.knowledge_loader import KnowledgeLoader; print('✅ 知识库加载成功')"

# 验证项目生成器
python -c "from src.embedded_freertos_mcp.generators.project_generator import ProjectGenerator; print('✅ 项目生成器就绪')"
```

## 💡 使用方法

### 1. MCP工具调用

在文心快码中通过自然语言调用工具：

#### 创建新项目
```
创建一个基于BK7252的智能家居网关项目
- 项目名称: smart_home_gateway
- 芯片型号: BK7252N
- 功能需求: WiFi连接、BLE通信、传感器数据采集
- 输出路径: ./my_projects
```

#### 获取芯片信息
```
查看BK7252芯片的详细规格和外设支持
```

#### 生成驱动代码
```
为BK7252生成UART和GPIO驱动代码
- 波特率: 115200
- GPIO引脚: PA0, PA1
```

### 2. 命令行使用

#### 直接运行MCP服务器
```bash
python -m src.embedded_freertos_mcp
```

#### 使用项目生成器
```python
from src.embedded_freertos_mcp.generators.project_generator import ProjectGenerator

# 初始化生成器
generator = ProjectGenerator("knowledge_base", "memory.db")

# 生成项目结构
project = generator.generate_project(
    project_name="test_project",
    chip_family="bk7252",
    output_path="./output"
)
```

### 3. API接口示例

#### 芯片分析
```python
from src.embedded_freertos_mcp.models.chip_analysis import ChipCapabilities

# 创建芯片能力模型
chip = ChipCapabilities(
    chip_family="BK7252",
    core="Cortex-M4",
    frequency=200000000,
    flash_size=2097152,
    ram_size=524288,
    peripherals=["UART", "SPI", "I2C", "GPIO", "PWM"]
)
```

#### 知识库查询
```python
from src.embedded_freertos_mcp.knowledge.knowledge_loader import KnowledgeLoader

loader = KnowledgeLoader("knowledge_base")
chip_info = loader.load_chip_config("bk7252")
```

## 🗂️ 项目架构

### 核心模块结构

```
src/
├── embedded_freertos_mcp/     # 主包
│   ├── __init__.py           # 包初始化
│   ├── server.py             # MCP服务器主程序
│   ├── main.py               # 命令行入口
│   ├── generators/           # 代码生成器
│   │   └── project_generator.py
│   ├── knowledge/           # 知识库管理
│   │   └── knowledge_loader.py
│   ├── memory/              # 记忆库管理
│   │   └── memory_manager.py
│   ├── models/              # 数据模型
│   │   └── chip_analysis.py
│   ├── templates/           # 代码模板
│   │   ├── projects/
│   │   │   ├── generic_template/
│   │   │   └── bk7252n_iot_gateway/
│   │   ├── drivers/
│   │   └── freertos/
│   └── tools/               # 工具集
│       ├── project_tools.py
│       ├── chip_analyzer.py
│       └── code_validator.py
├── generators/              # 独立生成器
│   └── template_manager.py
└── tools/                  # 独立工具
    └── code_validator.py
```

### 知识库结构

```
knowledge_base/
├── datasheets/             # 芯片规格书
│   ├── bk/                # BK系列芯片文档
│   │   ├── bk7252_summary.txt
│   │   └── parameters.yaml
│   ├── stm32/             # STM32系列文档
│   └── esp32/             # ESP32系列文档
├── sdks/                  # 原厂SDK
│   ├── bk7252_sdk/        # BK7252 SDK文档
│   └── stm32f4_sdk/       # STM32F4 SDK文档
├── requirements/           # 项目需求文档
│   ├── 项目需求.txt        # 总体需求规范
│   └── functional_docs/   # 功能详细文档
└── freertos/              # FreeRTOS文档
    ├── api_reference/
    └── best_practices/
```

### 配置系统

```
config/
├── mcu_configs/           # 芯片配置文件
│   ├── bk7252.yaml       # BK7252配置
│   └── stm32f4.yaml      # STM32F4配置
├── compiler_configs/      # 编译器配置
│   └── gcc_arm.yaml      # GCC ARM配置
└── validation_rules/      # 验证规则
    └── memory_rules.yaml # 内存验证规则
```

## 🎯 支持的芯片平台

### 当前支持的芯片

| 芯片型号 | 架构 | 主频 | Flash | RAM | 特性 |
|---------|------|------|-------|-----|------|
| **BK7252N** | Cortex-M4 | 200MHz | 2MB | 512KB | WiFi/BLE, 丰富外设 |
| **STM32F407** | Cortex-M4 | 168MHz | 1MB | 192KB | 高性能, 丰富外设 |
| **ESP32-S3** | Xtensa LX7 | 240MHz | 8MB | 512KB | 双核, WiFi/BLE |
| **GD32F450** | Cortex-M4 | 200MHz | 1MB | 256KB | 国产替代, 兼容STM32 |

### 扩展支持计划
- ✅ **已完成**: BK7252, STM32F4基础支持
- 🔄 **进行中**: ESP32系列深度集成
- 📅 **计划中**: RISC-V架构芯片支持

## 📁 生成的项目结构

### 标准项目模板

```
smart_home_gateway/           # 项目根目录
├── src/                      # 源代码目录
│   ├── main.c               # 应用程序主入口
│   ├── system.c             # 系统初始化和配置
│   ├── system.h             # 系统头文件
│   ├── tasks/               # FreeRTOS任务代码
│   │   ├── wifi_task.c      # WiFi连接任务
│   │   ├── ble_task.c       # BLE通信任务
│   │   └── sensor_task.c    # 传感器数据采集任务
│   └── drivers/             # 外设驱动
│       ├── uart_driver.c    # UART驱动
│       ├── gpio_driver.c    # GPIO驱动
│       └── i2c_driver.c     # I2C驱动
├── inc/                      # 头文件目录
│   ├── config.h             # 项目配置头文件
│   ├── task_config.h         # 任务配置
│   └── peripheral_config.h  # 外设配置
├── freertos/                 # FreeRTOS源码
│   ├── Config/              # FreeRTOS配置
│   ├── Source/              # FreeRTOS核心源码
│   └── portable/            # 移植层代码
├── build/                    # 构建输出目录
├── scripts/                 # 构建脚本
├── Makefile                 # 主构建文件
├── linker_script.ld         # 链接脚本
└── README.md                # 项目说明文档
```

### 项目配置文件示例

#### config.h
```c
#ifndef CONFIG_H
#define CONFIG_H

// FreeRTOS配置
#define configUSE_PREEMPTION        1
#define configCPU_CLOCK_HZ          200000000
#define configTICK_RATE_HZ          1000
#define configTOTAL_HEAP_SIZE       (50 * 1024)

// 外设配置
#define UART_BAUD_RATE              115200
#define WIFI_SSID                   "MyNetwork"
#define SENSOR_UPDATE_INTERVAL      1000

#endif
```

## 记忆库功能

- **保存项目配置**: 自动保存项目设置到SQLite数据库
- **加载历史项目**: 快速恢复之前的开发状态
- **芯片知识积累**: 持续学习芯片特性和最佳实践

## 开发工具

集成以下开发工具：

- **GCC ARM编译**: 使用arm-none-eabi-gcc
- **Make构建系统**: 自动化编译流程
- **调试支持**: 支持J-Link/ST-Link调试器
- **内存分析**: 堆栈使用情况分析

## 🔍 故障排除与调试

### 常见问题解决方案

#### 1. 模块导入错误
**问题**: `ModuleNotFoundError: No module named 'yaml'`
**解决**: 
```bash
pip install pyyaml
# 或者使用内置的JSON备选方案（已实现容错）
```

#### 2. 工具链路径问题
**问题**: 找不到arm-none-eabi-gcc
**解决**:
```bash
# 检查工具链安装
which arm-none-eabi-gcc

# 添加环境变量（Linux/macOS）
export PATH=$PATH:/path/to/gcc-arm/bin

# Windows系统路径设置
set PATH=%PATH%;C:\msys64\mingw64\bin
```

#### 3. 知识库文件缺失
**问题**: 芯片配置文件不存在
**解决**:
```bash
# 检查知识库结构
ls knowledge_base/datasheets/

# 添加缺失的芯片配置
cp config/mcu_configs/template.yaml config/mcu_configs/new_chip.yaml
```

#### 4. 权限问题（Windows）
**问题**: 文件访问被拒绝
**解决**:
- 以管理员权限运行命令行
- 检查文件权限设置
- 关闭防病毒软件的实时保护

### 调试模式

启用详细日志输出：
```bash
# 设置环境变量
export EMBEDDED_FREERTOS_DEBUG=1

# 或直接运行调试模式
python -m src.embedded_freertos_mcp --debug
```

### 日志文件位置
- **应用日志**: `logs/embedded_freertos_mcp.log`
- **错误日志**: `logs/error.log`
- **调试日志**: `logs/debug.log` (当启用调试模式时)

## 🤝 贡献指南

### 开发环境设置
```bash
# 1. Fork项目
git clone https://github.com/your-fork/embedded_freertos_mcp.git

# 2. 创建开发分支
git checkout -b feature/new-feature

# 3. 安装开发依赖
pip install -r requirements-dev.txt

# 4. 运行测试
python -m pytest tests/

# 5. 提交更改
git commit -m "添加新功能"
git push origin feature/new-feature
```

### 代码规范
- 遵循PEP 8代码风格
- 使用类型注解
- 添加详细的文档字符串
- 编写单元测试

### 提交Pull Request
1. 确保所有测试通过
2. 更新相关文档
3. 提供清晰的变更描述
4. 关联相关Issue

## 📞 支持与反馈

### 问题报告
如果您遇到问题，请提供：
1. 操作系统和Python版本
2. 详细的错误信息
3. 复现步骤
4. 相关日志文件

### 联系方式
- **GitHub Issues**: [项目Issues页面]
- **文档**: 查看本项目Wiki
- **社区**: 嵌入式开发技术论坛

## 📄 许可证

本项目采用MIT许可证。详见[LICENSE](LICENSE)文件。

## 🙏 致谢

感谢以下开源项目的贡献：
- **FreeRTOS**: 实时操作系统内核
- **Jinja2**: 模板引擎
- **Pydantic**: 数据验证
- **SQLite**: 轻量级数据库

---

**嵌入式FreeRTOS MCP扩展** - 让嵌入式开发更智能、更高效！ 🚀

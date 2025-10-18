# 文心快码嵌入式FreeRTOS MCP扩展使用指南

## 概述

这是一个专为文心快码设计的MCP扩展，用于自动化嵌入式FreeRTOS开发。当您说"我要用BK7252芯片做一个嵌入式FreeRTOS系统"时，智能体会：

1. **自动读取芯片知识库** - 查看BK7252的规格书、SDK和项目需求
2. **分析系统需求** - 根据功能文档确定所需的外设和任务
3. **生成完整项目** - 创建包含FreeRTOS内核、外设驱动、构建系统的完整项目
4. **保存配置到记忆库** - 记录项目设置，支持后续持续开发

## 快速开始

### 1. 安装扩展

```bash
# 克隆项目
git clone <repository-url>
cd embedded_freertos_mcp

# 安装依赖
pip install -r requirements.txt

# 测试安装
python scripts/demo.py
```

### 2. 配置文心快码

在VS Code的文心快码设置中添加：

```json
{
  "mcpServers": {
    "embedded-freertos": {
      "command": "python",
      "args": ["scripts/start_server.py"],
      "cwd": "/path/to/embedded_freertos_mcp"
    }
  }
}
```

### 3. 使用示例

在文心快码中输入：

```
创建嵌入式FreeRTOS项目
- 项目名称: my_bk7252_project  
- 芯片系列: bk7252
- 输出目录: ./projects
```

## 功能特性

### 智能知识库集成

- **芯片规格书**: 自动读取BK7252技术参数
- **原厂SDK**: 集成博通官方开发套件
- **项目需求**: 根据功能文档生成对应代码

### 自动化项目生成

- **FreeRTOS配置**: 自动配置任务调度、内存管理
- **外设驱动**: 生成GPIO、UART、SPI、I2C等驱动模板
- **构建系统**: 创建Makefile和链接脚本
- **内存优化**: 根据芯片RAM大小优化堆栈分配

### 记忆库功能

- **项目历史**: 保存每个项目的配置参数
- **最佳实践**: 积累开发经验，越用越智能
- **快速恢复**: 支持从记忆库重新加载项目

## 支持芯片

### 当前支持
- **BK7252N**: 博通集成WiFi/BLE的Cortex-M4 MCU
- **STM32F4**: 意法半导体高性能系列
- **ESP32**: 乐鑫WiFi/BLE双模芯片

### 计划支持
- Nordic nRF52系列
- TI CC系列
- 其他主流嵌入式MCU

## 项目结构

生成的项目包含：

```
项目名称/
├── src/                 # 源代码
│   ├── main.c          # 主程序
│   ├── system.c        # 系统配置
│   └── tasks/          # FreeRTOS任务
├── inc/                # 头文件
├── drivers/            # 外设驱动
│   ├── gpio/          # GPIO驱动
│   ├── uart/          # 串口驱动
│   └── ...
├── freertos/           # FreeRTOS内核
├── build/              # 构建输出
├── Makefile            # 构建脚本
└── linker_script.ld    # 链接脚本
```

## 开发流程

### 1. 项目创建
智能体自动分析需求，生成基础项目框架

### 2. 功能开发
- 使用文心快码智能补全编写业务逻辑
- MCP扩展提供外设驱动模板
- 实时验证代码正确性

### 3. 构建调试
- 一键编译生成固件
- 支持J-Link/ST-Link调试
- 内存使用分析

### 4. 部署测试
- 烧录到目标硬件
- 功能验证和性能测试

## 高级功能

### 自定义知识库
您可以在`knowledge_base`目录中添加：
- 新的芯片规格书
- 公司内部开发规范
- 特定应用场景的需求文档

### 模板定制
修改`src/embedded_freertos_mcp/templates`中的模板文件，定制代码风格和项目结构。

### 插件扩展
通过实现新的工具类，扩展MCP功能：
- 代码静态分析
- 性能优化建议
- 安全审计功能

## 故障排除

### 常见问题

**Q: MCP服务器无法启动**
A: 检查Python路径和依赖安装

**Q: 芯片配置加载失败**  
A: 确认knowledge_base目录结构正确

**Q: 项目生成错误**
A: 查看日志文件，检查文件权限

### 获取帮助
- 运行`python scripts/test_mcp.py`进行诊断
- 查看项目README.md文档
- 提交Issue到项目仓库

## 贡献指南

欢迎贡献代码、文档或测试用例：
1. Fork项目仓库
2. 创建功能分支
3. 提交Pull Request
4. 通过代码审查

## 许可证

MIT License - 详见LICENSE文件

---

*让嵌入式开发更智能，让文心快码成为您的嵌入式开发助手！*
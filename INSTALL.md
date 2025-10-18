# 安装部署指南

本文档提供嵌入式FreeRTOS MCP扩展的详细安装部署说明。

## 🚀 快速开始

### 系统要求检查

在开始安装前，请确保您的系统满足以下要求：

```bash
# 检查Python版本
python --version
# 应该显示 Python 3.8 或更高版本

# 检查pip版本
pip --version
```

### 一键安装脚本（Linux/macOS）

```bash
#!/bin/bash
# install.sh

echo "开始安装嵌入式FreeRTOS MCP扩展..."

# 检查Python
if ! command -v python &> /dev/null; then
    echo "错误: 未找到Python，请先安装Python 3.8+"
    exit 1
fi

# 检查pip
if ! command -v pip &> /dev/null; then
    echo "错误: 未找到pip，请先安装pip"
    exit 1
fi

# 安装依赖
echo "安装Python依赖..."
pip install -r requirements.txt

# 创建必要的目录
echo "创建项目目录..."
mkdir -p logs projects

# 验证安装
echo "验证安装..."
python -c "
try:
    from src.embedded_freertos_mcp.models.chip_analysis import ChipCapabilities
    from src.embedded_freertos_mcp.knowledge.knowledge_loader import KnowledgeLoader
    print('✅ 核心模块导入成功')
except Exception as e:
    print(f'❌ 导入失败: {e}')
    exit(1)
"

echo "✅ 安装完成！"
```

### Windows安装脚本

```powershell
# install.ps1
Write-Host "开始安装嵌入式FreeRTOS MCP扩展..." -ForegroundColor Green

# 检查Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "错误: 未找到Python，请先安装Python 3.8+" -ForegroundColor Red
    exit 1
}

# 检查pip
if (-not (Get-Command pip -ErrorAction SilentlyContinue)) {
    Write-Host "错误: 未找到pip，请先安装pip" -ForegroundColor Red
    exit 1
}

# 安装依赖
Write-Host "安装Python依赖..." -ForegroundColor Yellow
pip install -r requirements.txt

# 创建目录
Write-Host "创建项目目录..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "logs"
New-Item -ItemType Directory -Force -Path "projects"

# 验证安装
Write-Host "验证安装..." -ForegroundColor Yellow
python -c "
try:
    from src.embedded_freertos_mcp.models.chip_analysis import ChipCapabilities
    from src.embedded_freertos_mcp.knowledge.knowledge_loader import KnowledgeLoader
    print('✅ 核心模块导入成功')
except Exception as e:
    print(f'❌ 导入失败: {e}')
    exit(1)
"

Write-Host "✅ 安装完成！" -ForegroundColor Green
```

## 🔧 开发工具链配置

### GCC ARM工具链安装

#### Windows (MSYS2)
```bash
# 安装MSYS2（如果尚未安装）
# 下载地址: https://www.msys2.org/

# 更新包管理器
pacman -Syu

# 安装GCC ARM工具链
pacman -S mingw-w64-x86_64-arm-none-eabi-gcc
pacman -S make

# 验证安装
arm-none-eabi-gcc --version
```

#### Ubuntu/Debian
```bash
# 添加ARM工具链PPA
sudo add-apt-repository ppa:team-gcc-arm-embedded/ppa
sudo apt-get update

# 安装工具链
sudo apt-get install gcc-arm-embedded
sudo apt-get install make

# 验证安装
arm-none-eabi-gcc --version
```

#### macOS (Homebrew)
```bash
# 安装Homebrew（如果尚未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装工具链
brew install arm-none-eabi-gcc
brew install make

# 验证安装
arm-none-eabi-gcc --version
```

### 环境变量配置

#### Linux/macOS
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export PATH=$PATH:/usr/local/arm-gcc/bin
export ARM_GCC_PATH=/usr/local/arm-gcc

# 重新加载配置
source ~/.bashrc
```

#### Windows
```cmd
# 添加到系统环境变量
setx PATH "%PATH%;C:\msys64\mingw64\bin"
setx ARM_GCC_PATH "C:\msys64\mingw64\bin"

# 重启命令行生效
```

## 📚 文心快码集成配置

### 方法一：自动配置脚本

```bash
# 运行配置脚本
python scripts/setup_mcp.py
```

### 方法二：手动配置

1. **打开文心快码设置**
2. **找到MCP服务器配置**
3. **添加新的MCP服务器**

```json
{
  "mcpServers": {
    "embedded-freertos": {
      "command": "python",
      "args": ["-m", "src.embedded_freertos_mcp"],
      "cwd": "/path/to/embedded_freertos_mcp"
    }
  }
}
```

### 方法三：环境变量配置

```bash
# 设置项目根目录
export EMBEDDED_FREERTOS_ROOT="/path/to/embedded_freertos_mcp"

# 设置知识库路径
export KNOWLEDGE_BASE_PATH="$EMBEDDED_FREERTOS_ROOT/knowledge_base"
```

## 🧪 安装验证

### 基本功能测试

```bash
# 测试1: 模块导入
python -c "
import sys
sys.path.append('.')
from src.embedded_freertos_mcp.server import FreeRTOSMCPServer
print('✅ MCP服务器导入成功')
"

# 测试2: 知识库加载
python -c "
import sys
sys.path.append('.')
from src.embedded_freertos_mcp.knowledge.knowledge_loader import KnowledgeLoader
loader = KnowledgeLoader('knowledge_base')
config = loader.load_chip_config('bk7252')
print(f'✅ 知识库加载成功: {len(config) if config else 0} 个配置项')
"

# 测试3: 项目生成
python -c "
import sys
sys.path.append('.')
from src.embedded_freertos_mcp.generators.project_generator import ProjectGenerator
generator = ProjectGenerator('knowledge_base', 'memory.db')
print('✅ 项目生成器初始化成功')
"
```

### 完整功能测试

```bash
# 运行完整测试套件
python -m pytest tests/ -v

# 或运行单个测试文件
python tests/test_knowledge_loader.py
python tests/test_project_generator.py
```

## 🔄 更新与升级

### 更新到最新版本

```bash
# 拉取最新代码
git pull origin main

# 更新依赖
pip install -r requirements.txt --upgrade

# 运行数据库迁移（如果需要）
python scripts/migrate_database.py
```

### 版本回滚

```bash
# 查看版本历史
git log --oneline

# 回滚到指定版本
git checkout <commit-hash>

# 重新安装依赖
pip install -r requirements.txt
```

## 🐛 常见问题解决

### 问题1: Python模块导入错误

**症状**: `ModuleNotFoundError: No module named 'src'`

**解决**:
```bash
# 确保在项目根目录运行
cd /path/to/embedded_freertos_mcp

# 添加当前目录到Python路径
export PYTHONPATH=$PYTHONPATH:$(pwd)

# 或者使用模块方式运行
python -m src.embedded_freertos_mcp
```

### 问题2: 权限错误

**症状**: `Permission denied`

**解决**:
```bash
# Linux/macOS: 修改文件权限
chmod +x scripts/*.py

# Windows: 以管理员身份运行PowerShell
```

### 问题3: 工具链找不到

**症状**: `arm-none-eabi-gcc: command not found`

**解决**:
```bash
# 检查工具链安装路径
which arm-none-eabi-gcc

# 如果未找到，重新安装或添加路径
export PATH=$PATH:/path/to/arm-gcc/bin
```

## 📊 系统监控

### 资源使用监控

```bash
# 监控Python进程
ps aux | grep python

# 监控内存使用
free -h

# 监控磁盘空间
df -h
```

### 日志文件位置

- **应用日志**: `logs/embedded_freertos_mcp.log`
- **错误日志**: `logs/error.log`
- **调试日志**: `logs/debug.log` (调试模式启用时)

## 📞 技术支持

如果遇到安装问题，请：

1. **查看日志文件**获取详细错误信息
2. **检查系统要求**是否满足
3. **参考故障排除章节**
4. **提交Issue**到项目仓库

---

**祝您安装顺利！** 🎉
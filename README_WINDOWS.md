# Windows下一键部署指南

本文档提供在Windows系统上快速部署嵌入式FreeRTOS MCP扩展的详细说明。

## 🚀 快速开始

### 方法一：一键部署（推荐）

1. **下载项目代码**
   ```bash
   git clone https://github.com/your-repo/embedded_freertos_mcp.git
   cd embedded_freertos_mcp
   ```

2. **运行一键部署脚本**
   ```cmd
   deploy_windows.bat
   ```

3. **按照提示完成安装**

### 方法二：分步安装

如果一键部署遇到问题，可以按照以下步骤手动安装。

## 📋 系统要求

### 最低要求
- **操作系统**: Windows 10/11 (64位)
- **内存**: 4GB RAM
- **磁盘空间**: 2GB 可用空间

### 软件要求
- **Python 3.8+** ([下载地址](https://www.python.org/downloads/))
- **Git** ([下载地址](https://git-scm.com/download/win))
- **MSYS2** (可选，用于GCC ARM工具链)

## 🔧 部署脚本说明

### 1. 主部署脚本 (`deploy_windows.bat`)

**功能**:
- 自动检查Python环境
- 安装所有依赖包
- 配置MSYS2和GCC ARM工具链
- 设置环境变量
- 生成文心快码配置文件
- 验证安装结果

**使用方法**:
```cmd
# 以管理员身份运行（推荐）
deploy_windows.bat
```

### 2. MSYS2安装脚本 (`setup_msys2.bat`)

**功能**:
- 自动下载和安装MSYS2
- 安装GCC ARM工具链
- 配置系统环境变量

**使用方法**:
```cmd
# 如果deploy_windows.bat检测到MSYS2缺失，会自动运行此脚本
setup_msys2.bat
```

### 3. 快速测试脚本 (`quick_test.bat`)

**功能**:
- 快速验证系统功能
- 检查模块导入
- 验证文件完整性
- 生成测试报告

**使用方法**:
```cmd
quick_test.bat
```

## 🛠️ 手动安装步骤

### 步骤1: 安装Python

1. 访问 [Python官网](https://www.python.org/downloads/)
2. 下载Python 3.8+ for Windows
3. 安装时勾选 "Add Python to PATH"
4. 验证安装:
   ```cmd
   python --version
   pip --version
   ```

### 步骤2: 安装MSYS2和GCC ARM

1. 运行MSYS2安装脚本:
   ```cmd
   setup_msys2.bat
   ```
2. 或手动安装:
   - 下载MSYS2: https://www.msys2.org/
   - 安装到 `C:\msys64`
   - 运行MSYS2终端，执行:
     ```bash
     pacman -Syu
     pacman -S mingw-w64-x86_64-arm-none-eabi-gcc make
     ```

### 步骤3: 运行主部署脚本

```cmd
deploy_windows.bat
```

## 📊 部署过程监控

### 日志文件
- **部署日志**: `deployment.log`
- **错误日志**: `deployment_errors.log`
- **测试日志**: `quick_test.log`

### 进度指示
部署脚本会显示实时进度:
- ✅ 检查Python环境
- 📦 安装依赖包
- 🔧 配置工具链
- 📁 创建目录结构
- ⚙️ 设置环境变量
- 🔍 验证安装

## 🐛 常见问题解决

### 问题1: Python未找到
**症状**: `'python' 不是内部或外部命令`
**解决**:
1. 重新安装Python，确保勾选 "Add Python to PATH"
2. 或手动添加Python到PATH:
   ```cmd
   setx PATH "%PATH%;C:\Python39"
   ```

### 问题2: 权限不足
**症状**: `Access denied` 或安装失败
**解决**: 以管理员身份运行命令提示符

### 问题3: 网络问题
**症状**: pip安装超时或失败
**解决**:
```cmd
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题4: MSYS2安装失败
**症状**: MSYS2下载或安装失败
**解决**:
1. 手动下载MSYS2安装程序
2. 运行 `setup_msys2.bat` 单独安装

## 🔍 安装验证

部署完成后，运行快速测试脚本验证安装:

```cmd
quick_test.bat
```

预期输出:
```
✅ Python环境 - 通过
✅ 数据模型导入 - 通过
✅ 知识库加载器 - 通过
✅ 项目生成器 - 通过
✅ MCP服务器 - 通过
✅ 模板管理器 - 通过
🎉 所有测试通过！系统运行正常
```

## ⚙️ 文心快码配置

部署脚本会自动生成配置文件 `wenxin_mcp_config.json`。

**手动配置步骤**:
1. 打开文心快码设置
2. 找到MCP服务器配置
3. 导入或手动添加配置:
   ```json
   {
     "mcpServers": {
       "embedded-freertos": {
         "command": "python",
         "args": ["-m", "src.embedded_freertos_mcp"],
         "cwd": "项目根目录路径"
       }
     }
   }
   ```

## 🔄 更新和卸载

### 更新到新版本
```cmd
git pull origin main
deploy_windows.bat
```

### 卸载
1. 删除项目文件夹
2. 删除环境变量:
   ```cmd
   setx EMBEDDED_FREERTOS_ROOT ""
   setx KNOWLEDGE_BASE_PATH ""
   ```
3. 从文心快码设置中移除MCP配置

## 📞 技术支持

如果遇到问题:

1. **查看日志文件**获取详细错误信息
2. **运行快速测试**定位问题模块
3. **检查系统要求**是否满足
4. **提交Issue**到项目仓库

---

**祝您部署顺利！** 🎉
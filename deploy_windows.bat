@echo off
chcp 65001 >nul
title 嵌入式FreeRTOS MCP扩展 - Windows一键部署脚本

echo.
echo ========================================
echo   嵌入式FreeRTOS MCP扩展 Windows部署脚本
echo ========================================
echo.

set LOG_FILE=deployment.log
set ERROR_FILE=deployment_errors.log

:: 记录日志函数
:log
echo [%date% %time%] %* >> "%LOG_FILE%"
echo %*
goto :eof

:: 记录错误函数
:error
echo [%date% %time%] ERROR: %* >> "%ERROR_FILE%"
echo ❌ ERROR: %*
goto :eof

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ⚠️  需要管理员权限运行某些操作
    echo 请以管理员身份运行此脚本
    pause
    exit /b 1
)

:: 主部署函数
call :log "开始部署嵌入式FreeRTOS MCP扩展..."

:: 1. 检查Python环境
call :log "检查Python环境..."
python --version >nul 2>&1
if %errorLevel% neq 0 (
    call :error "未找到Python，请先安装Python 3.8+"
    echo.
    echo 📥 请从以下地址下载并安装Python:
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

python -c "import sys; print(sys.version)" >nul 2>&1
if %errorLevel% neq 0 (
    call :error "Python环境异常"
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%i in ('python -c "import sys; print(sys.version)" ^| findstr /r "^3\.[8-9]\|^3\.1[0-9]"') do (
    set PYTHON_VERSION=%%i
)
if "%PYTHON_VERSION%"=="" (
    call :error "需要Python 3.8或更高版本，当前版本不满足要求"
    pause
    exit /b 1
)

call :log "✅ Python版本检查通过: %PYTHON_VERSION%"

:: 2. 检查pip
call :log "检查pip环境..."
pip --version >nul 2>&1
if %errorLevel% neq 0 (
    call :error "未找到pip，请检查Python安装"
    pause
    exit /b 1
)

call :log "✅ pip环境检查通过"

:: 3. 安装Python依赖
call :log "安装Python依赖包..."
echo 📦 正在安装依赖包，这可能需要几分钟...

pip install --upgrade pip >> "%LOG_FILE%" 2>&1
if %errorLevel% neq 0 (
    call :error "pip升级失败"
    goto :install_deps_manual
)

:install_deps_manual
if exist requirements.txt (
    pip install -r requirements.txt >> "%LOG_FILE%" 2>&1
    if %errorLevel% neq 0 (
        call :error "依赖包安装失败，尝试逐个安装..."
        
        pip install pyyaml >> "%LOG_FILE%" 2>&1
        pip install pydantic >> "%LOG_FILE%" 2>&1
        pip install typing-extensions >> "%LOG_FILE%" 2>&1
        pip install jinja2 >> "%LOG_FILE%" 2>&1
    )
) else (
    call :error "requirements.txt文件不存在"
    pause
    exit /b 1
)

call :log "✅ Python依赖安装完成"

:: 4. 检查MSYS2环境
call :log "检查MSYS2环境..."
where msys2 >nul 2>&1
if %errorLevel% equ 0 (
    set MSYS2_FOUND=true
    call :log "✅ MSYS2已安装"
) else (
    set MSYS2_FOUND=false
    call :log "⚠️  未找到MSYS2，将跳过工具链安装"
)

:: 5. 安装GCC ARM工具链（如果MSYS2存在）
if "%MSYS2_FOUND%"=="true" (
    call :log "安装GCC ARM工具链..."
    echo 🔧 正在安装ARM工具链...
    
    :: 通过MSYS2安装工具链
    msys2 -c "pacman -Syu --noconfirm" >> "%LOG_FILE%" 2>&1
    msys2 -c "pacman -S --noconfirm mingw-w64-x86_64-arm-none-eabi-gcc" >> "%LOG_FILE%" 2>&1
    msys2 -c "pacman -S --noconfirm make" >> "%LOG_FILE%" 2>&1
    
    :: 检查工具链安装
    msys2 -c "arm-none-eabi-gcc --version" >> "%LOG_FILE%" 2>&1
    if %errorLevel% equ 0 (
        call :log "✅ GCC ARM工具链安装成功"
    ) else (
        call :error "GCC ARM工具链安装失败"
    )
)

:: 6. 创建必要目录
call :log "创建项目目录结构..."
if not exist logs mkdir logs
if not exist projects mkdir projects
if not exist build mkdir build

call :log "✅ 目录结构创建完成"

:: 7. 设置环境变量
call :log "设置环境变量..."
setx EMBEDDED_FREERTOS_ROOT "%CD%" >nul 2>&1
setx KNOWLEDGE_BASE_PATH "%CD%\knowledge_base" >nul 2>&1

:: 添加到PATH（当前会话）
set PATH=%PATH%;%CD%

call :log "✅ 环境变量设置完成"

:: 8. 验证安装
call :log "验证安装结果..."
echo 🔍 正在进行安装验证...

:: 测试模块导入
python -c "
import sys
sys.path.append('.')
try:
    from src.embedded_freertos_mcp.models.chip_analysis import ChipCapabilities
    print('✅ 数据模型导入成功')
except Exception as e:
    print(f'❌ 数据模型导入失败: {e}')
    sys.exit(1)
" >> "%LOG_FILE%" 2>&1

if %errorLevel% neq 0 (
    call :error "数据模型导入测试失败"
    goto :verification_failed
)

python -c "
import sys
sys.path.append('.')
try:
    from src.embedded_freertos_mcp.knowledge.knowledge_loader import KnowledgeLoader
    print('✅ 知识库加载器导入成功')
except Exception as e:
    print(f'❌ 知识库加载器导入失败: {e}')
    sys.exit(1)
" >> "%LOG_FILE%" 2>&1

if %errorLevel% neq 0 (
    call :error "知识库加载器导入测试失败"
    goto :verification_failed
)

python -c "
import sys
sys.path.append('.')
try:
    from src.embedded_freertos_mcp.server import FreeRTOSMCPServer
    print('✅ MCP服务器导入成功')
except Exception as e:
    print(f'❌ MCP服务器导入失败: {e}')
    sys.exit(1)
" >> "%LOG_FILE%" 2>&1

if %errorLevel% neq 0 (
    call :error "MCP服务器导入测试失败"
    goto :verification_failed
)

call :log "✅ 所有核心模块验证通过"

:: 9. 生成文心快码配置
call :log "生成文心快码配置文件..."
echo 📋 生成文心快码配置...

set MCP_CONFIG_FILE=wenxin_mcp_config.json

echo { > "%MCP_CONFIG_FILE%"
echo   "mcpServers": { >> "%MCP_CONFIG_FILE%"
echo     "embedded-freertos": { >> "%MCP_CONFIG_FILE%"
echo       "command": "python", >> "%MCP_CONFIG_FILE%"
echo       "args": ["-m", "src.embedded_freertos_mcp"], >> "%MCP_CONFIG_FILE%"
echo       "cwd": "%CD%" >> "%MCP_CONFIG_FILE%"
echo     } >> "%MCP_CONFIG_FILE%"
echo   } >> "%MCP_CONFIG_FILE%"
echo } >> "%MCP_CONFIG_FILE%"

call :log "✅ 文心快码配置文件生成完成: %MCP_CONFIG_FILE%"

:: 10. 部署完成
call :log "部署完成!"
echo.
echo ========================================
echo           🎉 部署成功完成!
echo ========================================
echo.
echo 📊 部署摘要:
echo ✅ Python环境检查通过
echo ✅ 依赖包安装完成
echo ✅ 项目目录结构创建
echo ✅ 环境变量配置完成
echo ✅ 核心模块验证通过
echo ✅ 文心快码配置文件生成
echo.
echo 📁 重要文件:
echo 📄 部署日志: %LOG_FILE%
echo ⚠️  错误日志: %ERROR_FILE%
echo ⚙️  文心快码配置: %MCP_CONFIG_FILE%
echo.
echo 🚀 下一步操作:
echo 1. 将文心快码配置文件导入到文心快码设置中
echo 2. 重启文心快码使配置生效
echo 3. 开始使用嵌入式FreeRTOS MCP扩展
echo.
echo 📞 如需帮助，请查看README.md和INSTALL.md文档
echo.

pause
exit /b 0

:verification_failed
call :error "安装验证失败，请检查日志文件"
echo.
echo ❌ 部署过程中出现问题
echo 📄 请查看日志文件: %LOG_FILE%
echo ⚠️  错误详情: %ERROR_FILE%
echo.
pause
exit /b 1
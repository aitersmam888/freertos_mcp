@echo off
chcp 65001 >nul
title 嵌入式FreeRTOS MCP扩展 - 快速测试脚本

echo.
echo ========================================
echo       快速功能测试脚本
echo ========================================
echo.

set TEST_LOG=quick_test.log

:: 记录测试结果
:test_result
echo [%time%] %* >> "%TEST_LOG%"
echo %*
goto :eof

:: 测试函数
:run_test
setlocal
set TEST_NAME=%~1
set TEST_CMD=%~2

echo 🔍 测试: %TEST_NAME%
echo [%time%] 测试: %TEST_NAME% >> "%TEST_LOG%"
echo 命令: %TEST_CMD% >> "%TEST_LOG%"

%TEST_CMD% >> "%TEST_LOG%" 2>&1
if %errorLevel% equ 0 (
    call :test_result "✅ %TEST_NAME% - 通过"
) else (
    call :test_result "❌ %TEST_NAME% - 失败"
)
endlocal
goto :eof

echo 开始快速功能测试...
echo.

:: 1. 测试Python环境
call :run_test "Python环境" "python --version"

:: 2. 测试模块导入
call :run_test "数据模型导入" "python -c \"import sys; sys.path.append('.'); from src.embedded_freertos_mcp.models.chip_analysis import ChipCapabilities; print('导入成功')\""

:: 3. 测试知识库加载
call :run_test "知识库加载器" "python -c \"import sys; sys.path.append('.'); from src.embedded_freertos_mcp.knowledge.knowledge_loader import KnowledgeLoader; print('加载器就绪')\""

:: 4. 测试项目生成器
call :run_test "项目生成器" "python -c \"import sys; sys.path.append('.'); from src.embedded_freertos_mcp.generators.project_generator import ProjectGenerator; print('生成器就绪')\""

:: 5. 测试MCP服务器
call :run_test "MCP服务器" "python -c \"import sys; sys.path.append('.'); from src.embedded_freertos_mcp.server import FreeRTOSMCPServer; print('服务器就绪')\""

:: 6. 测试模板系统
call :run_test "模板管理器" "python -c \"import sys; sys.path.append('.'); from src.generators.template_manager import TemplateManager; print('模板系统就绪')\""

:: 7. 测试知识库文件存在性
if exist "knowledge_base\datasheets\bk\bk7252_summary.txt" (
    call :test_result "✅ BK7252知识库文件 - 存在"
) else (
    call :test_result "❌ BK7252知识库文件 - 缺失"
)

:: 8. 测试配置文件
if exist "config\mcu_configs\bk7252.yaml" (
    call :test_result "✅ BK7252配置文件 - 存在"
) else (
    call :test_result "❌ BK7252配置文件 - 缺失"
)

:: 9. 测试模板文件
if exist "src\embedded_freertos_mcp\templates\projects\generic_template\main.c.j2" (
    call :test_result "✅ 项目模板文件 - 存在"
) else (
    call :test_result "❌ 项目模板文件 - 缺失"
)

echo.
echo ========================================
echo           📊 测试结果摘要
echo ========================================
echo.
type "%TEST_LOG%"
echo.
echo 📄 详细日志: %TEST_LOG%
echo.

:: 检查总体结果
findstr /C:"❌" "%TEST_LOG%" >nul
if %errorLevel% equ 0 (
    echo ⚠️  发现一些问题，请检查日志文件
) else (
    echo 🎉 所有测试通过！系统运行正常
)

echo.
pause
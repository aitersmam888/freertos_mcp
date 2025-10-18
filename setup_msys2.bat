@echo off
chcp 65001 >nul
title MSYS2和GCC ARM工具链安装脚本

echo.
echo ========================================
echo      MSYS2和GCC ARM工具链安装脚本
echo ========================================
echo.

set LOG_FILE=msys2_install.log
set MSYS2_URL=https://github.com/msys2/msys2-installer/releases/download/2023-11-30/msys2-x86_64-20231130.exe
set MSYS2_INSTALLER=msys2-installer.exe
set MSYS2_PATH=C:\msys64

:: 检查是否已安装MSYS2
if exist "%MSYS2_PATH%\msys2.exe" (
    echo ✅ MSYS2已安装于: %MSYS2_PATH%
    goto :install_toolchain
)

echo 📥 下载MSYS2安装程序...
powershell -Command "Invoke-WebRequest -Uri '%MSYS2_URL%' -OutFile '%MSYS2_INSTALLER%'" >nul 2>&1

if not exist "%MSYS2_INSTALLER%" (
    echo ❌ MSYS2下载失败
    pause
    exit /b 1
)

echo 🔧 安装MSYS2...
start /wait "" "%MSYS2_INSTALLER%" --confirm-command --accept-messages --root "%MSYS2_PATH%"

if not exist "%MSYS2_PATH%\msys2.exe" (
    echo ❌ MSYS2安装失败
    pause
    exit /b 1
)

echo ✅ MSYS2安装完成

:install_toolchain
echo 🔧 安装GCC ARM工具链...

:: 更新MSYS2包管理器
echo 📦 更新包管理器...
"%MSYS2_PATH%\msys2.exe" -c "pacman -Syu --noconfirm" >> "%LOG_FILE%" 2>&1

:: 安装GCC ARM工具链
echo 📦 安装ARM工具链...
"%MSYS2_PATH%\msys2.exe" -c "pacman -S --noconfirm mingw-w64-x86_64-arm-none-eabi-gcc" >> "%LOG_FILE%" 2>&1
"%MSYS2_PATH%\msys2.exe" -c "pacman -S --noconfirm make" >> "%LOG_FILE%" 2>&1
"%MSYS2_PATH%\msys2.exe" -c "pacman -S --noconfirm git" >> "%LOG_FILE%" 2>&1

:: 验证安装
"%MSYS2_PATH%\msys2.exe" -c "arm-none-eabi-gcc --version" >> "%LOG_FILE%" 2>&1
if %errorLevel% equ 0 (
    echo ✅ GCC ARM工具链安装成功
) else (
    echo ❌ GCC ARM工具链安装失败
    pause
    exit /b 1
)

:: 添加到系统PATH
echo 🔧 配置环境变量...
setx PATH "%PATH%;%MSYS2_PATH%\mingw64\bin" >nul 2>&1

echo ✅ 环境变量配置完成

:: 清理安装文件
if exist "%MSYS2_INSTALLER%" del "%MSYS2_INSTALLER%"

echo.
echo ========================================
echo           🎉 MSYS2安装完成!
echo ========================================
echo.
echo 📊 安装摘要:
echo ✅ MSYS2安装位置: %MSYS2_PATH%
echo ✅ GCC ARM工具链已安装
echo ✅ 环境变量已配置
echo.
echo 🔧 工具链路径: %MSYS2_PATH%\mingw64\bin
echo.
echo 📞 现在可以运行 deploy_windows.bat 继续部署
echo.

pause
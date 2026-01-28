@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

:: LTWin Manager 快速启动脚本
:: 用于自动检查依赖、创建虚拟环境并启动应用

echo.
echo ============================================
echo        LTWin Manager 快速启动脚本
echo ============================================
echo.

:: 检查Python是否已安装
echo [1/6] 正在检查Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python。请先安装Python 3.8或更高版本。
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%i in ('python --version 2^>^&1') do set python_version=%%i
echo 当前Python版本: !python_version!

:: 检查Python版本是否符合要求
for /f "tokens=1,2,3 delims=." %%a in ("!python_version!") do (
    set major=%%a
    set minor=%%b
    set patch=%%c
)

if !major! lss 3 (
    echo 错误: Python版本过低，需要Python 3.8或更高版本。
    pause
    exit /b 1
)

if !major! equ 3 if !minor! lss 8 (
    echo 错误: Python版本过低，需要Python 3.8或更高版本。
    pause
    exit /b 1
)

:: 检查pip是否可用
echo [2/6] 正在检查pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到pip。请确保Python安装时包含了pip。
    pause
    exit /b 1
)

:: 设置项目目录
set "PROJECT_DIR=%~dp0"
set "VENV_DIR=%PROJECT_DIR%.venv"

echo [3/6] 检查虚拟环境...

:: 检查虚拟环境是否存在
if not exist "%VENV_DIR%" (
    echo 虚拟环境不存在，正在创建...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo 错误: 创建虚拟环境失败。
        pause
        exit /b 1
    )
    echo 虚拟环境创建成功。
) else (
    echo 虚拟环境已存在。
)

:: 激活虚拟环境
call "%VENV_DIR%\Scripts\activate.bat"

:: 检查requirements.txt是否存在
if not exist "%PROJECT_DIR%requirements.txt" (
    echo 创建requirements.txt文件...
    echo PyQt6>=6.4.0> "%PROJECT_DIR%requirements.txt"
    echo PyQt6-Qt6>=6.4.0>> "%PROJECT_DIR%requirements.txt"
    echo PyQt6-sip>=13.4.0>> "%PROJECT_DIR%requirements.txt"
    echo psutil>=5.9.0>> "%PROJECT_DIR%requirements.txt"
    echo requests>=2.28.0>> "%PROJECT_DIR%requirements.txt"
    echo SQLAlchemy>=2.0.0>> "%PROJECT_DIR%requirements.txt"
    echo paramiko>=3.0.0>> "%PROJECT_DIR%requirements.txt"
)

:: 检查并安装依赖
echo [4/6] 检查并安装依赖...

:: 升级pip
echo 正在升级pip...
python -m pip install --upgrade pip >nul 2>&1

:: 读取requirements.txt并逐个检查依赖
set "MISSING_DEPS="
for /f "delims=" %%i in (%PROJECT_DIR%requirements.txt) do (
    set "dep=%%i"
    :: 跳过空行和注释
    if not "!dep!"=="" if not "!dep:~0,1!"=="#" (
        :: 提取包名（去掉版本号部分）
        for /f "tokens=1 delims=>=<!~" %%j in ("!dep!") do (
            set "pkg=%%j"
            if not "!pkg!"=="" (
                echo 检查包: !pkg!
                python -c "import !pkg.replace('-', '_')!" >nul 2>&1 || python -c "import !pkg!" >nul 2>&1
                if errorlevel 1 (
                    echo 包 !pkg! 缺失或安装不正确
                    set "MISSING_DEPS=!MISSING_DEPS! !pkg!"
                )
            )
        )
    )
)

:: 如果有缺失的依赖，进行安装
if not "!MISSING_DEPS!"=="" (
    echo 发现缺失的依赖: !MISSING_DEPS!
    echo 正在安装依赖...
    python -m pip install -r "%PROJECT_DIR%requirements.txt"
    if errorlevel 1 (
        echo 错误: 安装依赖失败。
        pause
        exit /b 1
    )
    echo 依赖安装完成。
) else (
    echo 所有依赖均已安装。
)

:: 检查QEMU是否已安装
echo [5/6] 检查QEMU虚拟化工具...
qemu-system-x86_64 --version >nul 2>&1
if errorlevel 1 (
    echo 警告: 未找到QEMU虚拟化工具。
    echo 请安装QEMU以支持虚拟机功能。
    echo 您可以从 https://www.qemu.org/download/ 下载QEMU。
    echo.
    set /p install_qemu="是否现在下载QEMU安装程序？(y/n): "
    if /i "!install_qemu!"=="y" (
        echo 正在打开QEMU下载页面...
        start "" "https://www.qemu.org/download/#windows"
    )
    echo.
) else (
    echo QEMU虚拟化工具已安装。
    for /f "delims=" %%i in ('qemu-system-x86_64 --version ^| findstr "version"') do echo %%i
)

:: 启动LTWin Manager
echo [6/6] 准备启动LTWin Manager
echo.
echo ============================================
echo        开始启动 LTWin Manager
echo ============================================
echo.

:: 检查是否已经创建了Python应用入口文件
if exist "%PROJECT_DIR%ltwin_manager\main.py" (
    echo 正在启动LTWin Manager完整版...
    cd /d "%PROJECT_DIR%"
    python -c "import sys; sys.path.insert(0, '.'); from ltwin_manager.main import main; main()" 
) else (
    echo LTWin Manager主程序未找到，启动测试版...
    if exist "%PROJECT_DIR%test_app.py" (
        python "%PROJECT_DIR%test_app.py"
    ) else (
        echo 注意: LTWin Manager主程序和测试程序均未找到。
        echo 请先运行 setup_project.py 创建项目结构。
        echo.
        echo 当前目录文件:
        dir /b
        echo.
        echo.
        echo 正在运行项目初始化...
        python "%PROJECT_DIR%setup_project.py"
        echo.
        echo 项目初始化完成，请重新运行此脚本。
    )
)

echo.
echo LTWin Manager 已退出
pause
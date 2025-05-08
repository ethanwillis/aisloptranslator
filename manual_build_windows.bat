@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo Manual Build Script for Clipboard Japanese Translator
echo ===================================================

:: Check if Python is installed
python --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Create a virtual environment
echo.
echo Creating virtual environment...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Could not create virtual environment, continuing with system Python
) else (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

:: Install required packages
echo.
echo Installing required packages...
python -m pip install --upgrade pip
python -m pip install pyinstaller==5.13.2 pyperclip googletrans==4.0.0-rc1 win10toast keyboard pywin32

:: Check for icon
if not exist icon.ico (
    echo.
    echo No icon.ico found. Creating a simple icon...
    echo Using Python to create a simple icon...
    python -c "import base64; icon = b'AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAABMLAAATCwAAAAAAAAAAAAD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wDAwMBAwMDAgMDAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDAgMDAwED///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8AwMDAQMDAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwED///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AMDAwIDAwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDAgP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wDAwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/////AP///wD///8A////AP///wD///8A////AP///wDAwMCAwMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDAgP///wD///8A////AP///wD///8A////AP///wDAwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP////8A////AP///wD///8A////AP///wDAwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP////8A////AP///wD///8A////AP///wDAwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP////8A////AP///wD///8A////AP///wDAwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP////8A////AP///wD///8A////AP///wDAwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP////8A////AP///wD///8A////AP///wDAwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP////8A////AP///wD///8A////AP///wDAwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP////8A////AP///wD///8A////AP///wDAwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP////8A////AP///wD///8A////AP///wDAwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP////8A////AP///wD///8A////AP///wDAwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP////8A////AP///wD///8A////AP///wDAwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP////8A////AP///wD///8A////AP///wDAwMCAwMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDAgP///wD///8A////AP///wD///8A////AP///wD///8AwMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/////AP///wD///8A////AP///wD///8A////AP///wD///8A////AMDAwIDAwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMCg////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8AwMDAQMDAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDAQP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8AwMDAQMDAwIDAwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMD/wMDA/8DAwP/AwMCAwMDAQP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A//////////////////////////////////////////4////8P///+B////gf///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///4P///+D////g////4////+f/////////////////////////8='; f = open('icon.ico', 'wb'); f.write(base64.b64decode(icon)); f.close()"
)

:: Create a spec file to avoid syntax errors
echo.
echo Creating PyInstaller spec file...
echo # -*- mode: python ; coding: utf-8 -*- > clipboard_translator.spec
echo. >> clipboard_translator.spec
echo block_cipher = None >> clipboard_translator.spec
echo. >> clipboard_translator.spec
echo a = Analysis( >> clipboard_translator.spec
echo     ['clipboard_translator_cross_platform.py'], >> clipboard_translator.spec
echo     pathex=[], >> clipboard_translator.spec
echo     binaries=[], >> clipboard_translator.spec
echo     datas=[('README.md', '.')], >> clipboard_translator.spec
echo     hiddenimports=['win32api', 'win32con'], >> clipboard_translator.spec
echo     hookspath=[], >> clipboard_translator.spec
echo     hooksconfig={}, >> clipboard_translator.spec
echo     runtime_hooks=[], >> clipboard_translator.spec
echo     excludes=[], >> clipboard_translator.spec
echo     win_no_prefer_redirects=False, >> clipboard_translator.spec
echo     win_private_assemblies=False, >> clipboard_translator.spec
echo     cipher=block_cipher, >> clipboard_translator.spec
echo     noarchive=False, >> clipboard_translator.spec
echo ) >> clipboard_translator.spec
echo. >> clipboard_translator.spec
echo pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher) >> clipboard_translator.spec
echo. >> clipboard_translator.spec
echo exe = EXE( >> clipboard_translator.spec
echo     pyz, >> clipboard_translator.spec
echo     a.scripts, >> clipboard_translator.spec
echo     a.binaries, >> clipboard_translator.spec
echo     a.zipfiles, >> clipboard_translator.spec
echo     a.datas, >> clipboard_translator.spec
echo     [], >> clipboard_translator.spec
echo     name='ClipboardJapaneseTranslator', >> clipboard_translator.spec
echo     debug=False, >> clipboard_translator.spec
echo     bootloader_ignore_signals=False, >> clipboard_translator.spec
echo     strip=False, >> clipboard_translator.spec
echo     upx=True, >> clipboard_translator.spec
echo     upx_exclude=[], >> clipboard_translator.spec
echo     runtime_tmpdir=None, >> clipboard_translator.spec
echo     console=False, >> clipboard_translator.spec
echo     disable_windowed_traceback=False, >> clipboard_translator.spec
echo     argv_emulation=False, >> clipboard_translator.spec
echo     target_arch=None, >> clipboard_translator.spec
echo     codesign_identity=None, >> clipboard_translator.spec
echo     entitlements_file=None, >> clipboard_translator.spec
echo     icon='icon.ico', >> clipboard_translator.spec
echo ) >> clipboard_translator.spec

:: Run PyInstaller
echo.
echo Building executable with PyInstaller...
echo This may take a few minutes...
python -m PyInstaller clipboard_translator.spec
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: PyInstaller failed.
    echo Attempting fallback build method...
    python -m PyInstaller --onefile --windowed --hidden-import=win32api --hidden-import=win32con --icon=icon.ico --add-data="README.md;." clipboard_translator_cross_platform.py
    
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Both build methods failed.
        echo.
        echo Troubleshooting tips:
        echo 1. Try installing Visual C++ Redistributable
        echo 2. Try updating PyInstaller: pip install pyinstaller --upgrade
        echo 3. Make sure you have administrator rights
        pause
        exit /b 1
    )
)

:: Check if build was successful
if exist dist\ClipboardJapaneseTranslator.exe (
    echo.
    echo ===================================================
    echo BUILD SUCCESSFUL!
    echo ===================================================
    echo.
    echo Executable created at:
    echo %CD%\dist\ClipboardJapaneseTranslator.exe
    echo.
    echo The executable contains all required dependencies and can be
    echo distributed to other Windows computers.
) else (
    echo.
    echo ===================================================
    echo BUILD FAILED!
    echo ===================================================
    echo.
    echo Could not locate executable in the expected location.
    echo Please check for errors above.
)

echo.
echo Press any key to exit...
pause > nul
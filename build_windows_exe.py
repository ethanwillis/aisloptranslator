import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['pyinstaller', 'pyperclip', 'googletrans==4.0.0-rc1', 'win10toast', 'keyboard', 'pywin32']
    
    for package in required_packages:
        try:
            if '==' in package:
                package_name = package.split('==')[0]
            else:
                package_name = package
            
            __import__(package_name)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is not installed. Installing...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✓ {package} has been installed")
            except Exception as e:
                print(f"Error installing {package}: {e}")
                print(f"Try manually installing: pip install {package}")

def clean_previous_builds():
    """Remove previous build folders if they exist"""
    directories_to_clean = ['build', 'dist']
    
    for directory in directories_to_clean:
        if os.path.exists(directory):
            print(f"Removing previous {directory} directory...")
            try:
                shutil.rmtree(directory)
            except Exception as e:
                print(f"Warning: Could not remove {directory}: {e}")
    
    # Remove spec files if they exist
    spec_files = ["clipboard_translator_cross_platform.spec", "clipboard_translator.spec"]
    for spec_file in spec_files:
        if os.path.exists(spec_file):
            print(f"Removing previous {spec_file} file...")
            try:
                os.remove(spec_file)
            except Exception as e:
                print(f"Warning: Could not remove {spec_file}: {e}")

def build_executable():
    """Build the executable using PyInstaller"""
    print("\nBuilding Windows executable...")
    
    # Define icon path
    icon_path = ""
    if os.path.exists("icon.ico"):
        icon_path = "--icon=icon.ico"
    
    # Create a PyInstaller spec file to avoid syntax errors
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['clipboard_translator_cross_platform.py'],
    pathex=[],
    binaries=[],
    datas=[('README.md', '.')],
    hiddenimports=['win32api', 'win32con'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ClipboardJapaneseTranslator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
    """
    
    # Write spec file
    with open("clipboard_translator.spec", "w") as f:
        f.write(spec_content)
    
    try:
        # Run PyInstaller with spec file
        subprocess.check_call([sys.executable, '-m', 'PyInstaller', 'clipboard_translator.spec'])
        print("Build completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error during PyInstaller build: {e}")
        print("\nTrying alternative build method...")
        
        # PyInstaller command-line approach as fallback
        pyinstaller_command = [
            sys.executable, '-m', 'PyInstaller',
            '--name=ClipboardJapaneseTranslator',
            '--onefile',
            '--windowed',  # No console window
            '--clean',
            '--hidden-import=win32api',
            '--hidden-import=win32con',
        ]
        
        if icon_path:
            pyinstaller_command.append(icon_path)
            
        pyinstaller_command.append('--add-data=README.md;.')
        pyinstaller_command.append('clipboard_translator_cross_platform.py')
        
        # Run PyInstaller
        subprocess.check_call(pyinstaller_command)

def create_installer():
    """Create an installer using NSIS (if available)"""
    try:
        # Check if NSIS is installed
        nsis_path = shutil.which("makensis")
        if nsis_path:
            print("\nNSIS found. Creating installer...")
            
            # Create NSIS script
            nsis_script = """
            !include "MUI2.nsh"
            
            ; Application information
            Name "Clipboard Japanese Translator"
            OutFile "ClipboardJapaneseTranslator_Setup.exe"
            InstallDir "$PROGRAMFILES\\ClipboardJapaneseTranslator"
            
            ; Interface settings
            !define MUI_ABORTWARNING
            !define MUI_ICON "icon.ico"
            !define MUI_UNICON "icon.ico"
            
            ; Pages
            !insertmacro MUI_PAGE_WELCOME
            !insertmacro MUI_PAGE_DIRECTORY
            !insertmacro MUI_PAGE_INSTFILES
            !insertmacro MUI_PAGE_FINISH
            
            !insertmacro MUI_UNPAGE_CONFIRM
            !insertmacro MUI_UNPAGE_INSTFILES
            
            ; Languages
            !insertmacro MUI_LANGUAGE "English"
            
            ; Installer sections
            Section "Install"
                SetOutPath "$INSTDIR"
                
                ; Include main executable
                File "dist\\ClipboardJapaneseTranslator.exe"
                
                ; Create start menu shortcut
                CreateDirectory "$SMPROGRAMS\\Clipboard Japanese Translator"
                CreateShortcut "$SMPROGRAMS\\Clipboard Japanese Translator\\Clipboard Japanese Translator.lnk" "$INSTDIR\\ClipboardJapaneseTranslator.exe"
                
                ; Create uninstaller
                WriteUninstaller "$INSTDIR\\Uninstall.exe"
                
                ; Add uninstall information to Add/Remove Programs
                WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\ClipboardJapaneseTranslator" "DisplayName" "Clipboard Japanese Translator"
                WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\ClipboardJapaneseTranslator" "UninstallString" "$\\"$INSTDIR\\Uninstall.exe$\\""
                WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\ClipboardJapaneseTranslator" "DisplayIcon" "$\\"$INSTDIR\\ClipboardJapaneseTranslator.exe$\\""
                WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\ClipboardJapaneseTranslator" "Publisher" "ClipboardJapaneseTranslator"
            SectionEnd
            
            ; Uninstaller section
            Section "Uninstall"
                ; Remove files
                Delete "$INSTDIR\\ClipboardJapaneseTranslator.exe"
                Delete "$INSTDIR\\Uninstall.exe"
                
                ; Remove shortcuts
                Delete "$SMPROGRAMS\\Clipboard Japanese Translator\\Clipboard Japanese Translator.lnk"
                RMDir "$SMPROGRAMS\\Clipboard Japanese Translator"
                
                ; Remove install directory
                RMDir "$INSTDIR"
                
                ; Remove registry entries
                DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\ClipboardJapaneseTranslator"
            SectionEnd
            """
            
            # Write NSIS script to file
            with open("installer.nsi", "w") as f:
                f.write(nsis_script)
            
            # Run NSIS to create installer
            subprocess.check_call(["makensis", "installer.nsi"])
            
            print("Installer created successfully: ClipboardJapaneseTranslator_Setup.exe")
        else:
            print("\nNSIS not found. Skipping installer creation.")
            print("You can install NSIS from https://nsis.sourceforge.io/Download")
    except Exception as e:
        print(f"Error creating installer: {e}")
        print("Skipping installer creation.")

def main():
    """Main function to build Windows executable"""
    print("=" * 50)
    print("Building Windows Executable for Clipboard Japanese Translator")
    print("=" * 50)
    
    try:
        # Check and install dependencies
        print("\nChecking dependencies...")
        check_dependencies()
        
        # Clean previous builds
        print("\nCleaning previous builds...")
        clean_previous_builds()
        
        # Build executable
        build_executable()
        
        # Create installer (optional)
        create_installer()
        
        print("\n" + "=" * 50)
        print("Build completed!")
        print(f"Executable located at: {os.path.abspath(os.path.join('dist', 'ClipboardJapaneseTranslator.exe'))}")
        print("=" * 50)
        
        print("\nNote: The executable includes all dependencies and can be distributed to other Windows computers.")
        print("You don't need to include any other files with it.")
    except Exception as e:
        print("\n" + "=" * 50)
        print(f"ERROR: Build failed with exception: {e}")
        print("=" * 50)
        
        # Print detailed error for debugging
        import traceback
        traceback.print_exc()
        
        print("\nTroubleshooting tips:")
        print("1. Try installing PyInstaller manually: pip install pyinstaller==5.13.2")
        print("2. Make sure you have Visual C++ Redistributable installed")
        print("3. Try running the script with administrator privileges")
        sys.exit(1)

if __name__ == "__main__":
    main()
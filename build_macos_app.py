import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def check_macos():
    """Check if running on macOS"""
    if platform.system() != "Darwin":
        print("This script must be run on macOS.")
        sys.exit(1)

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['py2app', 'pyperclip', 'googletrans==4.0.0-rc1', 'pynput', 'pync']
    
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
                print("Please install it manually: pip install " + package)
                sys.exit(1)

def clean_previous_builds():
    """Remove previous build folders if they exist"""
    directories_to_clean = ['build', 'dist']
    
    for directory in directories_to_clean:
        if os.path.exists(directory):
            print(f"Removing previous {directory} directory...")
            shutil.rmtree(directory)
    
    # Remove py2app setup file if it exists
    setup_file = "setup.py"
    if os.path.exists(setup_file):
        print(f"Removing previous {setup_file} file...")
        os.remove(setup_file)

def create_setup_py():
    """Create setup.py file for py2app"""
    setup_content = """
from setuptools import setup

APP = ['clipboard_translator_cross_platform.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',
    'plist': {
        'CFBundleName': 'Clipboard Japanese Translator',
        'CFBundleDisplayName': 'Clipboard Japanese Translator',
        'CFBundleGetInfoString': 'Translate clipboard text to Japanese',
        'CFBundleIdentifier': 'com.clipboardtranslator.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2023',
        'NSAppleEventsUsageDescription': 'This app needs access to run AppleScript',
        'NSAppleMusicUsageDescription': 'This app uses AppleEvents',
        'NSCalendarsUsageDescription': 'This app uses Calendar access',
        'NSCameraUsageDescription': 'This app needs camera access',
        'NSMicrophoneUsageDescription': 'This app needs microphone access',
        'NSAccessibilityUsageDescription': 'This app needs accessibility to monitor keyboard input',
    },
    'packages': ['tkinter', 'pyperclip', 'googletrans', 'pynput', 'pync'],
    'includes': ['tkinter', 'pyperclip', 'googletrans', 'pynput', 'pync', 'platform', 'subprocess', 'threading'],
}

setup(
    name='Clipboard Japanese Translator',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
"""
    with open("setup.py", "w") as f:
        f.write(setup_content)
    
    print("Created setup.py for py2app")

def check_icon():
    """Check if icon file exists, create a dummy one if not"""
    if not os.path.exists("icon.icns"):
        print("No icon.icns file found. The app will use the default Python icon.")
        print("To use a custom icon, place an icon.icns file in the current directory.")
        print("You can convert a PNG to ICNS using iconutil or online converters.")

def build_app():
    """Build the macOS app using py2app"""
    print("\nBuilding macOS application...")
    
    # First, try with development mode to test
    try:
        subprocess.check_call([sys.executable, 'setup.py', 'py2app', '-A'])
        print("Development build created successfully.")
    except Exception as e:
        print(f"Development build failed: {e}")

    # Then do a full build
    try:
        print("\nCreating production build (this may take a while)...")
        subprocess.check_call([sys.executable, 'setup.py', 'py2app'])
        print("Production build created successfully.")
    except Exception as e:
        print(f"Production build failed: {e}")
        sys.exit(1)

def add_accessibility_entitlements():
    """Add Accessibility entitlements to the app"""
    print("\nAdding accessibility entitlements...")
    
    app_path = "dist/Clipboard Japanese Translator.app"
    
    if not os.path.exists(app_path):
        print(f"Error: Could not find the app at {app_path}")
        return
    
    # Create entitlements file
    entitlements_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.automation.apple-events</key>
    <true/>
    <key>com.apple.security.device.audio-input</key>
    <true/>
    <key>com.apple.security.device.camera</key>
    <true/>
    <key>com.apple.security.personal-information.addressbook</key>
    <true/>
    <key>com.apple.security.personal-information.calendars</key>
    <true/>
    <key>com.apple.security.personal-information.location</key>
    <true/>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.allow-dyld-environment-variables</key>
    <true/>
    <key>com.apple.security.cs.disable-library-validation</key>
    <true/>
    <key>com.apple.security.cs.disable-executable-page-protection</key>
    <true/>
    <key>com.apple.security.cs.debugger</key>
    <true/>
    <key>com.apple.security.get-task-allow</key>
    <true/>
    <key>com.apple.security.device.bluetooth</key>
    <true/>
</dict>
</plist>"""
    
    with open("entitlements.plist", "w") as f:
        f.write(entitlements_content)
    
    print("Created entitlements.plist")
    
    # Try to sign the app if codesign is available
    try:
        # Find the main executable within the app bundle
        app_executable = os.path.join(app_path, "Contents/MacOS/Clipboard Japanese Translator")
        
        # Run codesign
        subprocess.check_call(["codesign", "--force", "--deep", "--sign", "-", 
                              "--entitlements", "entitlements.plist", app_executable])
        
        print("App signed with entitlements successfully")
    except Exception as e:
        print(f"Could not sign app with entitlements: {e}")
        print("You may need to manually add entitlements or sign the app.")

def create_dmg():
    """Create a DMG installer for the app"""
    print("\nCreating DMG installer...")
    
    app_path = "dist/Clipboard Japanese Translator.app"
    dmg_path = "dist/Clipboard-Japanese-Translator.dmg"
    
    if not os.path.exists(app_path):
        print(f"Error: Could not find the app at {app_path}")
        return False
    
    try:
        # Check if create-dmg is installed
        if shutil.which("create-dmg"):
            # Create DMG using create-dmg
            subprocess.check_call([
                "create-dmg",
                "--volname", "Clipboard Japanese Translator",
                "--window-pos", "200", "100",
                "--window-size", "800", "500",
                "--icon-size", "100",
                "--icon", "Clipboard Japanese Translator.app", "200", "200",
                "--hide-extension", "Clipboard Japanese Translator.app",
                "--app-drop-link", "600", "200",
                dmg_path,
                app_path
            ])
            print(f"DMG created successfully at {dmg_path}")
            return True
        elif shutil.which("hdiutil"):
            # Fallback to using hdiutil directly
            temp_dmg = "dist/temp.dmg"
            subprocess.check_call([
                "hdiutil", "create", "-volname", "Clipboard Japanese Translator",
                "-srcfolder", app_path, "-ov", "-format", "UDRW", temp_dmg
            ])
            subprocess.check_call([
                "hdiutil", "convert", temp_dmg, "-format", "UDZO", "-o", dmg_path
            ])
            os.remove(temp_dmg)
            print(f"DMG created successfully at {dmg_path}")
            return True
        else:
            print("Neither create-dmg nor hdiutil found. Cannot create DMG.")
            print("You can install create-dmg with: brew install create-dmg")
            return False
    except Exception as e:
        print(f"Error creating DMG: {e}")
        return False

def main():
    """Main function to build macOS application"""
    print("=" * 50)
    print("Building macOS Application for Clipboard Japanese Translator")
    print("=" * 50)
    
    # Check if running on macOS
    check_macos()
    
    # Check and install dependencies
    print("\nChecking dependencies...")
    check_dependencies()
    
    # Clean previous builds
    print("\nCleaning previous builds...")
    clean_previous_builds()
    
    # Create setup.py for py2app
    create_setup_py()
    
    # Check for icon file
    check_icon()
    
    # Build the app
    build_app()
    
    # Add accessibility entitlements
    add_accessibility_entitlements()
    
    # Create DMG installer
    create_dmg()
    
    print("\n" + "=" * 50)
    print("Build completed!")
    print(f"Application located at: {os.path.abspath('dist/Clipboard Japanese Translator.app')}")
    print("=" * 50)
    
    print("\nINSTRUCTIONS FOR USERS:")
    print("1. When first launching the app, macOS will ask for permissions")
    print("2. Go to System Preferences > Security & Privacy > Privacy > Accessibility")
    print("3. Add the Clipboard Japanese Translator app to the list of allowed apps")
    print("4. Restart the app after granting permissions")

if __name__ == "__main__":
    main()
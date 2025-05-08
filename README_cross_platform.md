# Cross-Platform Clipboard Japanese Translator

This application allows you to translate text from your clipboard into Japanese instantly with a global hotkey. The translated text is automatically copied back to your clipboard. The application works on both Windows and macOS.

## Features

- **Cross-Platform Compatibility**: Works on both Windows and macOS
- **Global Hotkey**:
  - Windows: Press `Ctrl+J` anywhere on your system to translate clipboard text
  - macOS: Press `⌘+J` (Command+J) anywhere on your system to translate clipboard text
- **System Notifications**: Get desktop notifications when translations are completed
- **GUI Interface**: Also includes a traditional application interface
- **Automatically reads text from your clipboard**
- **Translates the text to Japanese using Google Translate**
- **Copies the translated text back to your clipboard**
- **Shows both the original text and the translation in the app**

## Installation

1. Make sure you have Python installed on your computer (3.6+ recommended)
2. Install the required packages:

```
pip install -r requirements_cross_platform.txt
```

The installer will automatically detect your operating system and install the appropriate packages.

## Usage

1. Run the application:

```
python clipboard_translator_cross_platform.py
```

2. Once launched, the application will register the appropriate hotkey for your system:
   - Windows: Ctrl+J
   - macOS: ⌘+J (Command+J)

3. To translate text:
   - Copy any text to your clipboard (Ctrl/⌘+C)
   - Press the hotkey anywhere (even when the app is minimized)
   - The translated Japanese text will be in your clipboard ready to be pasted (Ctrl/⌘+V)
   - A desktop notification will show a preview of the translation

4. You can also use the app interface:
   - Copy text to clipboard
   - Click the "Translate Clipboard" button in the app

5. Additional controls:
   - Toggle the global hotkey on/off with the button in the app
   - Close the application properly using the window close button (×) to release the hotkey

## Requirements

### Core Requirements (All Platforms)
- Python 3.6+
- pyperclip: Clipboard access
- googletrans: Translation (version 4.0.0-rc1)
- tkinter: For the GUI interface (included with most Python installations)

### Windows-Specific Requirements
- keyboard: For global hotkey functionality
- win10toast: For desktop notifications

### macOS-Specific Requirements
- pynput: For global hotkey functionality
- pync: For desktop notifications

## Notes

- **Windows**: The application may require administrator privileges to register global hotkeys
- **macOS**: The application will need accessibility permissions:
  1. Go to System Preferences > Security & Privacy > Privacy > Accessibility
  2. Add your terminal or Python application to the list of allowed applications
- The application uses the unofficial googletrans library which may have reliability issues if Google changes their API
- If translations stop working, you may need to update the library or switch to an official translation API with authentication
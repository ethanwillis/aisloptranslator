# Clipboard Japanese Translator

A cross-platform application to translate text in your clipboard to Japanese with a single hotkey press.

## Features

- Translate clipboard text to Japanese with a hotkey (Ctrl+J on Windows, ⌘+J on macOS)
- Desktop notifications when translation completes
- Simple GUI interface
- Cross-platform (Windows, macOS)

## Usage

1. Copy any text to your clipboard
2. Press the hotkey (Ctrl+J on Windows, ⌘+J on macOS) or click the "Translate Clipboard" button
3. The translated Japanese text will be copied to your clipboard automatically
4. A notification will appear showing a preview of the translation

## Building From Source

### Requirements

- Python 3.6 or higher
- Required Python packages (installed automatically by build scripts):
  - `pyperclip`
  - `googletrans==4.0.0-rc1`
  - Platform-specific packages:
    - Windows: `win10toast`, `keyboard`
    - macOS: `pynput`, `pync`

### Windows

To build a standalone Windows executable:

1. Run the build script:
   ```
   python build_windows_exe.py
   ```

2. The executable will be created in the `dist` folder as `ClipboardJapaneseTranslator.exe`

3. If NSIS is installed, an installer will also be created as `ClipboardJapaneseTranslator_Setup.exe`

### macOS

To build a macOS application bundle:

1. Run the build script:
   ```
   python build_macos_app.py
   ```

2. The application will be created in the `dist` folder as `Clipboard Japanese Translator.app`

3. A DMG installer may also be created if you have `create-dmg` or `hdiutil` installed

### macOS Permissions

On macOS, the application requires Accessibility permissions to detect the hotkey:

1. When first launching the app, macOS will prompt for permissions
2. Go to System Preferences > Security & Privacy > Privacy > Accessibility
3. Add the Clipboard Japanese Translator app to the list of allowed apps
4. Restart the app after granting permissions

## Running Without Building

You can run the application directly with Python:

```
python clipboard_translator_cross_platform.py
```

## Troubleshooting

### Windows Issues

- If the hotkey doesn't work, try running the application as Administrator
- Some applications may block global hotkeys

### macOS Issues

- If the hotkey doesn't work, check that Accessibility permissions are granted
- If you see "This process is not trusted!", grant accessibility permissions
- If you're running from a virtual environment, the app may be in fallback mode with no hotkey support

### General Issues

- If the translation doesn't work, check your internet connection
- The Google Translate API may have rate limits or require updates over time

## License

This project is open source and available under the MIT License.
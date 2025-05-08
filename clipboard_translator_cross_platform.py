import tkinter as tk
from tkinter import messagebox  # Import messagebox explicitly
import pyperclip
from googletrans import Translator
import threading
import sys
import platform

# Detect operating system
OS_SYSTEM = platform.system()

# Platform-specific imports
if OS_SYSTEM == "Windows":
    import keyboard
    from win10toast import ToastNotifier
    # Initialize Windows notifier
    toaster = ToastNotifier()
    HOTKEY = 'ctrl+j'
    HOTKEY_DISPLAY = "Ctrl+J"
    
elif OS_SYSTEM == "Darwin":  # macOS
    # Use a try/except to handle potential import issues
    try:
        import pynput.keyboard as pynput_keyboard
        import subprocess
        from pync import Notifier
        import os.path
        # Set flag for pynput availability
        PYNPUT_AVAILABLE = True
    except Exception as e:
        print(f"Warning: Could not import pynput or other macOS modules: {e}")
        # Fallback mode without pynput
        PYNPUT_AVAILABLE = False
        
    HOTKEY = "<cmd>+j"  # For display purposes only
    HOTKEY_DISPLAY = "⌘+J"
    # Mac hotkey listener will be initialized later
    mac_hotkey_listener = None
    # Accessibility permission check variables
    mac_permissions_ok = False
else:
    # For Linux or other platforms - basic fallback
    HOTKEY = 'ctrl+j'
    HOTKEY_DISPLAY = "Ctrl+J"

# Global variables
keybind_active = True

# Function to show notifications based on platform
# Show notification
def show_notification(title, message, duration=3):
    if OS_SYSTEM == "Windows":
        toaster.show_toast(title, message, duration=duration, threaded=True)
    elif OS_SYSTEM == "Darwin":
        try:
            if PYNPUT_AVAILABLE:
                # Use pync for Mac notifications
                Notifier.notify(message, title=title)
            else:
                # Use applescript as fallback for notifications
                script = f'display notification "{message}" with title "{title}"'
                subprocess.run(["osascript", "-e", script], capture_output=True)
        except Exception as e:
            print(f"Mac notification error: {e}")
            # Last resort fallback - print to console
            print(f"{title}: {message}")
    else:
        # Fallback for other platforms - print to console
        print(f"{title}: {message}")

# Core translation function
def translate_clipboard(show_notification_flag=True):
    # Get text from clipboard
    clipboard_text = pyperclip.paste()
    
    # Check if clipboard has text
    if not clipboard_text:
        if show_notification_flag:
            show_notification("Clipboard Japanese Translator", "Clipboard is empty")
        if 'root' in globals() and root.winfo_exists() and root.winfo_viewable():
            result_label.config(text="Clipboard is empty")
        return
    
    # Translate text to Japanese
    translator = Translator()
    try:
        translation = translator.translate(clipboard_text, dest='ja')
        translated_text = translation.text
        
        # Copy translated text back to clipboard
        pyperclip.copy(translated_text)
        
        # Update UI if window exists and is visible
        if 'root' in globals() and root.winfo_exists() and root.winfo_viewable():
            original_text.delete(1.0, tk.END)
            original_text.insert(tk.END, clipboard_text)
            
            translated_display.delete(1.0, tk.END)
            translated_display.insert(tk.END, translated_text)
            
            result_label.config(text="Translated and copied to clipboard!")
        
        # Show notification
        if show_notification_flag:
            # Truncate long text for notification
            orig_preview = (clipboard_text[:25] + '...') if len(clipboard_text) > 28 else clipboard_text
            trans_preview = (translated_text[:25] + '...') if len(translated_text) > 28 else translated_text
            notification_text = f"Original: {orig_preview}\nTranslated: {trans_preview}"
            show_notification("Text Translated to Japanese", notification_text)
            
        return translated_text
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        if show_notification_flag:
            show_notification("Translation Error", error_msg)
        if 'root' in globals() and root.winfo_exists() and root.winfo_viewable():
            result_label.config(text=error_msg)
        return None

# Function that gets called when hotkey is pressed
def hotkey_handler():
    if keybind_active:
        # Use a thread to avoid freezing the keyboard handling
        threading.Thread(target=translate_clipboard).start()

# Check if macOS accessibility permissions are granted
def check_mac_accessibility_permissions():
    if not PYNPUT_AVAILABLE:
        return False
        
    try:
        # Create a dummy listener just to test permissions
        # Don't actually start it to avoid potential crashes
        test_listener = pynput_keyboard.Listener(on_press=lambda key: None)
        # Just check if we can create it without errors
        return True
    except Exception as e:
        print(f"Accessibility permissions check: {e}")
        return False

# Mac-specific hotkey handler
def on_mac_hotkey_press(key):
    if not PYNPUT_AVAILABLE:
        return
        
    try:
        # Check if Command+J is pressed
        if key == pynput_keyboard.Key.cmd:
            # Set command key flag
            on_mac_hotkey_press.cmd_pressed = True
        elif hasattr(key, 'char') and key.char == 'j' and getattr(on_mac_hotkey_press, 'cmd_pressed', False):
            # Command+J detected
            if keybind_active:
                threading.Thread(target=translate_clipboard).start()
    except Exception as e:
        # Don't print error messages for permission denied errors
        if "accessibility" not in str(e) and "trusted" not in str(e):
            print(f"Error in Mac hotkey handler: {e}")

def on_mac_hotkey_release(key):
    if not PYNPUT_AVAILABLE:
        return
        
    if key == pynput_keyboard.Key.cmd:
        # Reset command key flag
        on_mac_hotkey_press.cmd_pressed = False

# Initialize Mac hotkey listener
def setup_mac_hotkeys():
    global mac_hotkey_listener, mac_permissions_ok
    
    if not PYNPUT_AVAILABLE:
        print("pynput module not available. Hotkeys will not work.")
        mac_permissions_ok = False
        return False
    
    # Check if we have accessibility permissions
    mac_permissions_ok = check_mac_accessibility_permissions()
    
    if not mac_permissions_ok:
        print("Accessibility permissions not granted. Hotkeys will not work.")
        return False
    
    try:
        # Set initial state
        on_mac_hotkey_press.cmd_pressed = False
        # Create listener
        mac_hotkey_listener = pynput_keyboard.Listener(
            on_press=on_mac_hotkey_press,
            on_release=on_mac_hotkey_release)
        # Start listening in a safer way
        mac_hotkey_listener.start()
        return True
    except Exception as e:
        print(f"Error setting up Mac hotkeys: {e}")
        mac_permissions_ok = False
        return False

# Function to toggle the hotkey on/off
def toggle_hotkey():
    global keybind_active
    keybind_active = not keybind_active
    toggle_button.config(text=f"{'Disable' if keybind_active else 'Enable'} {HOTKEY_DISPLAY} Hotkey")
    status_var.set(f"Hotkey status: {'Active' if keybind_active else 'Disabled'}")

# Function to restart Mac permissions
def restart_mac_permissions():
    global mac_permissions_ok, mac_hotkey_listener
    
    if not PYNPUT_AVAILABLE:
        messagebox.showerror("Module Not Available", 
                           "The pynput module is not available or could not be loaded.\n\n"
                           "Hotkeys will not work, but you can still use the 'Translate Clipboard' button.")
        return
    
    try:
        # Check permissions again
        mac_permissions_ok = check_mac_accessibility_permissions()
        
        if mac_permissions_ok:
            # Success - permissions granted
            retry_button.pack_forget()  # Hide retry button
            if setup_mac_hotkeys():  # Setup hotkeys
                toggle_button.pack(side=tk.LEFT, padx=5)  # Show toggle button
                messagebox.showinfo("Permissions Granted", 
                                  "Accessibility permissions detected!\n\nYou can now use ⌘+J hotkey from anywhere.")
                status_var.set("Hotkey status: Active")
            else:
                status_var.set("Hotkey status: Setup failed")
                messagebox.showinfo("Setup Issue", 
                                  "Permissions appear to be granted but hotkey setup failed.\n\nPlease restart the application.")
        else:
            # Still no permissions
            messagebox.showerror("Permissions Required", 
                               "Accessibility permissions are still not granted.\n\nPlease follow the instructions to enable them.")
    except Exception as e:
        print(f"Error in restart_mac_permissions: {e}")
        messagebox.showerror("Error", f"Error checking permissions: {str(e)}")

# Function to exit the application
def exit_app():
    try:
        if OS_SYSTEM == "Windows":
            keyboard.unhook_all()  # Release Windows keyboard hooks
        elif OS_SYSTEM == "Darwin" and PYNPUT_AVAILABLE and mac_hotkey_listener:
            mac_hotkey_listener.stop()  # Stop Mac listener
    except Exception as e:
        print(f"Error releasing keyboard hooks: {e}")
    
    root.destroy()
    sys.exit()

# Create the main window
root = tk.Tk()
root.title("Clipboard Japanese Translator")
root.geometry("600x550")
root.configure(bg="#f0f0f0")
root.protocol("WM_DELETE_WINDOW", exit_app)  # Handle window close event

# Add NSApplicationSupportsSecureRestorableState flag to silence warning
if OS_SYSTEM == "Darwin":
    try:
        # This silences the warning about secure coding for restorable state on macOS
        root.createcommand('::tk::mac::NSApplicationSupportsSecureRestorableState', lambda: 1)
    except Exception as e:
        # Ignore if this fails, it's just to silence a warning
        print(f"Note: Could not set NSApplicationSupportsSecureRestorableState: {e}")
    
    # Additional Mac-specific UI tweaks
    try:
        # Set app name in menu bar (macOS)
        root.createcommand('::tk::mac::Preferences', lambda: None)  # Disable preferences menu item
        root.option_add('*tearOff', False)  # Disable tear-off menus
    except:
        pass  # Ignore errors, these are just UI enhancements

# Create a frame for better organization
main_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# Title label
title_label = tk.Label(
    main_frame, 
    text="Clipboard to Japanese Translator", 
    font=("Arial", 16, "bold"),
    bg="#f0f0f0"
)
title_label.pack(pady=10)

# Instructions
instructions = tk.Label(
    main_frame,
    text=f"Press {HOTKEY_DISPLAY} anywhere to translate text from clipboard\nor click 'Translate' button below.",
    font=("Arial", 10),
    bg="#f0f0f0",
    justify=tk.CENTER
)
instructions.pack(pady=5)

# Hotkey status
status_var = tk.StringVar(value=f"Hotkey status: {'Active' if keybind_active else 'Disabled'}")
status_label = tk.Label(
    main_frame,
    textvariable=status_var,
    font=("Arial", 9),
    bg="#f0f0f0",
    fg="#007700"
)
status_label.pack(pady=2)

# Original text frame
original_frame = tk.LabelFrame(main_frame, text="Original Text", bg="#f0f0f0", padx=10, pady=10)
original_frame.pack(fill=tk.BOTH, expand=True, pady=10)

original_text = tk.Text(original_frame, wrap=tk.WORD, height=6)
original_text.pack(fill=tk.BOTH, expand=True)

# Translated text frame
translated_frame = tk.LabelFrame(main_frame, text="Japanese Translation", bg="#f0f0f0", padx=10, pady=10)
translated_frame.pack(fill=tk.BOTH, expand=True, pady=10)

translated_display = tk.Text(translated_frame, wrap=tk.WORD, height=6)
translated_display.pack(fill=tk.BOTH, expand=True)

# Button frame
button_frame = tk.Frame(main_frame, bg="#f0f0f0")
button_frame.pack(pady=10)

# Translate button
translate_button = tk.Button(
    button_frame,
    text="Translate Clipboard",
    command=lambda: translate_clipboard(),
    font=("Arial", 12),
    bg="#4CAF50",
    fg="white",
    padx=10,
    pady=5
)
translate_button.pack(side=tk.LEFT, padx=5)

# Toggle hotkey button
toggle_button = tk.Button(
    button_frame,
    text=f"Disable {HOTKEY_DISPLAY} Hotkey",
    command=toggle_hotkey,
    font=("Arial", 12),
    bg="#FF9800",
    fg="white",
    padx=10,
    pady=5
)

# Only display the toggle button if hotkeys are available
if not (OS_SYSTEM == "Darwin" and not mac_permissions_ok):
    toggle_button.pack(side=tk.LEFT, padx=5)
else:
    # Update status label to show permissions are needed
    status_var.set("Hotkey status: Permissions required")

# Result label
result_label = tk.Label(main_frame, text="", font=("Arial", 10), bg="#f0f0f0")
result_label.pack(pady=5)

# Permission retry button for macOS (initially hidden)
retry_button = tk.Button(
    main_frame,
    text="Retry After Granting Permissions",
    command=lambda: restart_mac_permissions(),
    font=("Arial", 10, "bold"),
    bg="#2196F3",
    fg="white",
    padx=10,
    pady=5
)
# Will be packed only if needed

# Platform-specific setup and messaging
try:
    if OS_SYSTEM == "Windows":
        # Register Windows global hotkey
        keyboard.add_hotkey('ctrl+j', hotkey_handler)
        print("Windows hotkey Ctrl+J registered successfully")
        startup_message = "The application is now running!\n\nPress Ctrl+J from anywhere to translate text in your clipboard to Japanese."
    
    elif OS_SYSTEM == "Darwin":  # macOS
        # Setup Mac global hotkeys
        try:
            if not PYNPUT_AVAILABLE:
                print("pynput module not available on macOS, running in fallback mode")
                startup_message = ("Running in limited mode - hotkeys not available.\n\n"
                                  "The pynput module couldn't be loaded. This can happen if:\n"
                                  "- You're running from a virtual environment\n"
                                  "- The module isn't installed correctly\n\n"
                                  "You can still use the 'Translate Clipboard' button, "
                                  "but hotkeys won't be available.")
                # Don't show retry button since pynput isn't available at all
            else:
                hotkey_setup_success = setup_mac_hotkeys()
                
                if hotkey_setup_success:
                    print("Mac hotkey ⌘+J listener started successfully")
                    startup_message = "The application is now running!\n\nPress ⌘+J (Command+J) from anywhere to translate text in your clipboard to Japanese."
                else:
                    print("Failed to register Mac hotkeys due to permissions")
                    startup_message = ("Accessibility Permissions Required\n\n"
                                      "To use keyboard shortcuts, this app needs accessibility permissions:\n"
                                      "1. Open System Preferences > Security & Privacy > Privacy\n"
                                      "2. Select 'Accessibility' from the sidebar\n"
                                      "3. Click the lock icon and enter your password\n"
                                      "4. Add and check this application\n"
                                      "5. Click the 'Retry After Granting Permissions' button\n\n"
                                      "Until then, you can still use the 'Translate Clipboard' button.")
                    
                    # Show retry button
                    retry_button.pack(pady=10, before=result_label)
        except Exception as e:
            print(f"Error setting up Mac hotkeys: {e}")
            startup_message = ("Error setting up keyboard shortcuts.\n\n"
                               "You can still use the 'Translate Clipboard' button.\n\n"
                               f"Error details: {str(e)}")
            
            # Show retry button
            retry_button.pack(pady=10, before=result_label)
    
    else:  # Linux or other platforms
        print("Hotkeys not supported on this platform")
        startup_message = "The application is now running!\n\nUse the Translate button to translate text in your clipboard to Japanese.\n\nNote: Global hotkeys are not supported on this platform."

    # Display a startup message
    messagebox.showinfo("Hotkey Registered", startup_message)
    
except Exception as e:
    error_message = f"Could not register hotkey: {str(e)}"
    print(error_message)
    messagebox.showerror("Error", error_message)

# Safer exception handling for main event loop
try:
    # Exit the application
    root.mainloop()
except Exception as e:
    print(f"Error in main application loop: {e}")
    try:
        import traceback
        traceback.print_exc()
    except:
        pass
import requests
import pyautogui
import time
import os
import subprocess
import sys
import pyperclip
from botcity.core import DesktopBot
import pygetwindow as gw

# --- 0️⃣ Safe Notepad Cleanup with Empty Check ---
def close_all_notepads():
    notepad_windows = [win for win in gw.getAllWindows() if 'notepad' in win.title.lower()]

    for win in notepad_windows:
        try:
            win.restore()
            win.activate()
            time.sleep(0.5)

            # Clear clipboard before copying
            pyperclip.copy("")

            # Select all and copy content
            pyautogui.hotkey("ctrl", "a")
            time.sleep(0.5)
            pyautogui.hotkey("ctrl", "c")
            time.sleep(0.5)

            content = pyperclip.paste().strip()

            if content:  
                # If Notepad has text → close with Don't Save
                pyautogui.hotkey("ctrl", "w")
                time.sleep(0.5)
                pyautogui.press("right")
                pyautogui.press("enter")
            else:
                # If Notepad is empty → just close
                pyautogui.hotkey("ctrl", "w")

            time.sleep(0.5)

        except Exception as e:
            print(f"Error closing Notepad: {e}")

    print("✅ All Notepad windows closed safely.")
    
# Run cleanup before anything else
close_all_notepads()

# --- 0.5️⃣ Ensure starting Notepad is empty ---
subprocess.Popen(["notepad.exe"])
time.sleep(1)  # wait for Notepad to open

# Clear any text (harmless if empty)
pyautogui.hotkey("ctrl", "a")
time.sleep(0.5)
pyautogui.press("delete")
time.sleep(0.5)

# Close the Notepad safely
pyautogui.hotkey("ctrl", "w")
time.sleep(0.5)
pyautogui.press("right")  # move to "Don't Save" if prompted
pyautogui.press("enter")
time.sleep(0.5)

print("✅ Starting Notepad cleared, ready for automation loop.")

# --- 1️⃣ Locate Desktop path (works with or without OneDrive) ---
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
onedrive_desktop_path = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")

# Prefer OneDrive Desktop if it exists
if os.path.exists(onedrive_desktop_path):
    project_folder = os.path.join(onedrive_desktop_path, "tjm-project")
else:
    project_folder = os.path.join(desktop_path, "tjm-project")

# ✅ Create folder if it doesn't exist
os.makedirs(project_folder, exist_ok=True)

# --- 2️⃣ Fetch posts from API ---
try:
    response = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=10)
    response.raise_for_status()
    posts = response.json()
except Exception as e:
    print(f"❌ Error fetching posts: {e}")
    sys.exit(1)

# --- 3️⃣ Main loop for first 10 posts ---
for i, post in enumerate(posts[:10], start=1):
    try:
        # Launch Notepad
        subprocess.Popen(["notepad.exe"])
        time.sleep(1)  # wait for Notepad to open

        # Type the Title and Body
        pyautogui.typewrite(f"Title: {post['title']}", interval=0.03)
        pyautogui.press("enter")
        pyautogui.press("enter")  # ensures two empty lines
        pyautogui.typewrite(f"Body: {post['body']}", interval=0.03)

        # Save the file
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1)  # wait for Save dialog
        file_path = os.path.join(project_folder, f"post {i}.txt")
        pyautogui.typewrite(file_path)
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(1)  # wait for saving

        print(f"✅ Saved: {file_path}")

        # --- Close Notepad immediately after saving ---
        bot = DesktopBot()
        element = bot.find("close_btn", matching=0.9, waiting_time=5000)
        if element:
            bot.click(element)
            bot.wait(1000)  # wait a bit before next loop
        else:
            print("⚠️ Could not find Notepad close button.")

    except Exception as e:
    # Only print if it’s NOT the harmless BotCity Box/float error
        if "unsupported operand type(s) for /: 'Box' and 'float'" not in str(e):
            print(f"❌ Error while processing post {i}: {e}")


print("✅ Finished processing all posts.")

import requests
import pyautogui
import time
import os
import subprocess
import sys
import pygetwindow as gw  # for graceful Notepad closing

# --- 0️⃣ Close all Notepad windows at the start ---
notepad_windows = [w for w in gw.getAllWindows() if 'notepad' in w.title.lower()]
for w in notepad_windows:
    w.close()
time.sleep(0.5)  # give them a moment to close

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
        pyautogui.press("enter")
        time.sleep(1)  # wait for saving

        print(f"✅ Saved: {file_path}")

    except Exception as e:
        print(f"❌ Error while processing post {i}: {e}")

# --- 4️⃣ Close all Notepad windows at the end (gracefully) ---
notepad_windows = [w for w in gw.getAllWindows() if 'notepad' in w.title.lower()]
for w in notepad_windows:
    w.close()
time.sleep(0.5)

print("✅ All Notepad windows closed.")

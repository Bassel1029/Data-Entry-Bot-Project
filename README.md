# Automated Data Entry Bot for Notepad

## Description
This Python project automates data entry into the desktop application **Notepad**. It fetches posts from the [JSONPlaceholder API](https://jsonplaceholder.typicode.com/) and writes them as text files, simulating a simple blog post workflow. Each post is saved individually in a designated folder on the Desktop.

## Features
- Automatically fetches the first 10 posts from JSONPlaceholder.
- Opens Notepad, types the post title and body with proper formatting.
- Saves each post as a text file (`post 1.txt`, `post 2.txt`, etc.) in a `tjm-project` directory on the Desktop.
- Gracefully handles multiple Notepad windows:
  - Closes any existing Notepad windows before starting.
  - Uses **BotCity** image recognition to find and click the Notepad close button.
- Error handling for network failures or file saving issues.
- Fully packageable as a standalone executable using PyInstaller.

## Technologies Used
- Python 3.x
- [PyAutoGUI](https://pyautogui.readthedocs.io/) for keyboard automation
- [PyGetWindow](https://pygetwindow.readthedocs.io/) for window management
- [Requests](https://docs.python-requests.org/) for API calls
- [BotCity Core](https://github.com/botcity-dev/botcity-framework-core) for image-based UI automation

## Setup & Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/automated-notepad-bot.git

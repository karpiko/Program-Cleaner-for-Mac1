# Mac Program Cleaner

A modern, Python-based application to clean your Mac. It allows you to uninstall applications completely (including associated files) and clean system junk.

## Features
- **App Uninstaller**: Finds and removes apps along with their preferences, caches, and support files.
- **System Cleaner**: Removes system caches and logs.
- **Secure Delete**: Files are permanently deleted, not just moved to Trash.
- **Modern UI**: Built with CustomTkinter for a sleek dark mode look.

## Installation

1.  **Install Python**: Ensure you have Python 3 installed.
    - You can download it from [python.org](https://www.python.org/downloads/).
2.  **Install Dependencies**:
    Open your terminal and run:
    ```bash
    pip3 install -r requirements.txt
    ```

## How to Open

You can easily run the app using the provided script:
```bash
./run_app.sh
```
Or manually:
```bash
python3 main.py
```

## How to Upload to GitHub

1.  **Create a Repository**:
    - Go to [GitHub](https://github.com) and create a new repository (e.g., "mac-program-cleaner").
    - Do **not** initialize with a README, .gitignore, or license (since you have them locally).

2.  **Initialize Git Locally**:
    Open your terminal in this folder and run:
    ```bash
    git init
    git add .
    git commit -m "Initial commit: Mac Program Cleaner App"
    ```

3.  **Push to GitHub**:
    Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual details.
    ```bash
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
    git push -u origin main
    ```

### Option 2: Using GitHub Desktop
1.  Open **GitHub Desktop**.
2.  Go to **File** > **Add Local Repository**.
3.  Choose the folder: `/Users/karpikonajak/Program Cleaner for Mac`.
4.  Click **Add Repository**.
5.  You will see a prompt saying "This directory does not appear to be a Git repository" (if you haven't run git init yet) or it will just add it.
    - If it asks to create one, click **Create a Repository**.
6.  Fill in the name and description, then click **Create Repository**.
7.  Click **Publish repository** in the top toolbar to push it to GitHub.

## Disclaimer
This app deletes files permanently. Use with caution. The author is not responsible for any data loss.

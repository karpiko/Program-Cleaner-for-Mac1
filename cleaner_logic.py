import os
import shutil
import glob
from pathlib import Path
import send2trash

class CleanerLogic:
    def __init__(self):
        self.user_home = str(Path.home())
        self.apps_dir = "/Applications"
        self.user_apps_dir = os.path.join(self.user_home, "Applications")
        
        # Common paths where apps store data
        self.library_paths = [
            os.path.join(self.user_home, "Library/Application Support"),
            os.path.join(self.user_home, "Library/Caches"),
            os.path.join(self.user_home, "Library/Preferences"),
            os.path.join(self.user_home, "Library/Saved Application State"),
            os.path.join(self.user_home, "Library/Logs"),
            os.path.join(self.user_home, "Library/Cookies"),
            os.path.join(self.user_home, "Library/Containers"),
            os.path.join(self.user_home, "Library/Group Containers"),
            os.path.join(self.user_home, "Library/WebKit"),
        ]

    def get_installed_apps(self):
        """Scans Applications folders for .app bundles."""
        apps = []
        for app_dir in [self.apps_dir, self.user_apps_dir]:
            if os.path.exists(app_dir):
                for item in os.listdir(app_dir):
                    if item.endswith(".app"):
                        apps.append(os.path.join(app_dir, item))
        return sorted(apps)

    def find_associated_files(self, app_path):
        """Finds files related to the app based on name and bundle ID guessing."""
        app_name = os.path.basename(app_path).replace(".app", "")
        # Simple normalization for search
        search_terms = [app_name, app_name.lower(), app_name.replace(" ", "")]
        
        found_files = []
        
        # 1. Check Library paths
        for lib_path in self.library_paths:
            if not os.path.exists(lib_path):
                continue
                
            try:
                for item in os.listdir(lib_path):
                    # Check if any search term is in the item name
                    if any(term in item for term in search_terms):
                        full_path = os.path.join(lib_path, item)
                        found_files.append(full_path)
            except PermissionError:
                continue
                
        return found_files

    def get_size(self, path):
        """Calculates size of file or directory."""
        total_size = 0
        try:
            if os.path.isfile(path):
                total_size = os.path.getsize(path)
            elif os.path.isdir(path):
                for dirpath, _, filenames in os.walk(path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        if not os.path.islink(fp):
                            total_size += os.path.getsize(fp)
        except Exception:
            pass
        return total_size

    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"

    def delete_item(self, path, secure=False):
        """Deletes a file or directory. 
        secure=True uses send2trash (safer) or actual shredding could be implemented.
        For this request 'without leaving any file', we might want direct deletion.
        But for safety, let's default to trash, and offer direct delete."""
        try:
            if secure:
                # "Secure" in this context means direct removal, bypassing trash
                if os.path.isfile(path) or os.path.islink(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
            else:
                # Move to trash
                send2trash.send2trash(path)
            return True, "Deleted"
        except Exception as e:
            return False, str(e)

    def get_system_junk(self):
        """Scans for common system junk."""
        junk_paths = [
            os.path.join(self.user_home, "Library/Caches"),
            os.path.join(self.user_home, "Library/Logs"),
            os.path.join(self.user_home, ".Trash"), # Be careful with this one
        ]
        
        junk_files = []
        for path in junk_paths:
            if os.path.exists(path):
                # We don't want to delete the folder itself, just contents
                try:
                    for item in os.listdir(path):
                        full_path = os.path.join(path, item)
                        junk_files.append(full_path)
                except PermissionError:
                    pass
        return junk_files

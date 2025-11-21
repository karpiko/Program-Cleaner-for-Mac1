import customtkinter as ctk
import threading
import os
from cleaner_logic import CleanerLogic
from tkinter import messagebox

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Mac Program Cleaner")
        self.geometry("900x600")

        # Set theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.cleaner = CleanerLogic()
        self.current_scan_results = []

        # Layout configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()

    def create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Mac Cleaner", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_uninstall = ctk.CTkButton(self.sidebar_frame, text="App Uninstaller", command=self.show_uninstall_page)
        self.btn_uninstall.grid(row=1, column=0, padx=20, pady=10)

        self.btn_system = ctk.CTkButton(self.sidebar_frame, text="System Junk", command=self.show_system_page)
        self.btn_system.grid(row=2, column=0, padx=20, pady=10)

    def create_main_area(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Initial Page
        self.show_uninstall_page()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_uninstall_page(self):
        self.clear_main_frame()
        
        title = ctk.CTkLabel(self.main_frame, text="App Uninstaller", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=10, anchor="w")

        scan_btn = ctk.CTkButton(self.main_frame, text="Scan Applications", command=self.start_app_scan)
        scan_btn.pack(pady=10, anchor="w")

        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame, label_text="Installed Applications")
        self.scrollable_frame.pack(fill="both", expand=True, pady=10)

    def show_system_page(self):
        self.clear_main_frame()
        
        title = ctk.CTkLabel(self.main_frame, text="System Junk", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=10, anchor="w")

        scan_btn = ctk.CTkButton(self.main_frame, text="Scan System Junk", command=self.start_system_scan)
        scan_btn.pack(pady=10, anchor="w")

        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame, label_text="Junk Files")
        self.scrollable_frame.pack(fill="both", expand=True, pady=10)

    def start_app_scan(self):
        # Clear previous results
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        loading_label = ctk.CTkLabel(self.scrollable_frame, text="Scanning...")
        loading_label.pack(pady=20)
        
        def scan_thread():
            apps = self.cleaner.get_installed_apps()
            self.after(0, lambda: self.display_apps(apps))

        threading.Thread(target=scan_thread, daemon=True).start()

    def display_apps(self, apps):
        # Clear loading
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not apps:
            ctk.CTkLabel(self.scrollable_frame, text="No apps found.").pack(pady=20)
            return

        for app_path in apps:
            app_name = os.path.basename(app_path)
            
            row_frame = ctk.CTkFrame(self.scrollable_frame)
            row_frame.pack(fill="x", pady=5, padx=5)
            
            label = ctk.CTkLabel(row_frame, text=app_name, anchor="w")
            label.pack(side="left", padx=10, pady=10)
            
            clean_btn = ctk.CTkButton(row_frame, text="Clean", width=80, 
                                      command=lambda p=app_path: self.confirm_clean_app(p))
            clean_btn.pack(side="right", padx=10)

    def confirm_clean_app(self, app_path):
        # Find associated files first
        associated_files = self.cleaner.find_associated_files(app_path)
        total_files = [app_path] + associated_files
        
        # Calculate size
        total_size = sum(self.cleaner.get_size(f) for f in total_files)
        size_str = self.cleaner.format_size(total_size)
        
        msg = f"Found {len(associated_files)} associated files.\nTotal size: {size_str}\n\nFiles to delete:\n"
        for f in total_files[:5]: # Show first 5
            msg += f"- {os.path.basename(f)}\n"
        if len(total_files) > 5:
            msg += f"...and {len(total_files)-5} more."
            
        # In a real app, we'd use a custom dialog. For now, simple print or we can add a dialog class.
        # Since standard messagebox might not work well with custom tkinter loop sometimes, 
        # let's create a simple Toplevel window for confirmation.
        self.open_confirm_dialog(msg, total_files)

    def open_confirm_dialog(self, message, files_to_delete):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirm Deletion")
        dialog.geometry("400x300")
        
        label = ctk.CTkLabel(dialog, text="Confirm Deletion", font=ctk.CTkFont(size=18, weight="bold"))
        label.pack(pady=10)
        
        msg_label = ctk.CTkTextbox(dialog, height=150)
        msg_label.pack(fill="x", padx=20, pady=10)
        msg_label.insert("0.0", message)
        msg_label.configure(state="disabled")
        
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        def delete_action():
            for f in files_to_delete:
                self.cleaner.delete_item(f, secure=True) # Using secure=True for direct delete as requested
            dialog.destroy()
            self.start_app_scan() # Refresh
            
        confirm_btn = ctk.CTkButton(btn_frame, text="DELETE PERMANENTLY", fg_color="red", hover_color="darkred", command=delete_action)
        confirm_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", command=dialog.destroy)
        cancel_btn.pack(side="right", padx=10)

    def start_system_scan(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        junk_files = self.cleaner.get_system_junk()
        
        if not junk_files:
            ctk.CTkLabel(self.scrollable_frame, text="System is clean!").pack(pady=20)
            return
            
        total_size = sum(self.cleaner.get_size(f) for f in junk_files)
        
        info_frame = ctk.CTkFrame(self.scrollable_frame)
        info_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(info_frame, text=f"Found {len(junk_files)} items. Total: {self.cleaner.format_size(total_size)}").pack(pady=10)
        
        clean_all_btn = ctk.CTkButton(self.scrollable_frame, text="Clean All System Junk", fg_color="red", hover_color="darkred",
                                      command=lambda: self.clean_system_junk(junk_files))
        clean_all_btn.pack(pady=10)
        
        # List some items
        for f in junk_files[:20]:
            ctk.CTkLabel(self.scrollable_frame, text=f, anchor="w").pack(fill="x", padx=10)
        if len(junk_files) > 20:
            ctk.CTkLabel(self.scrollable_frame, text=f"...and {len(junk_files)-20} more").pack(pady=5)

    def clean_system_junk(self, files):
        for f in files:
            self.cleaner.delete_item(f, secure=True)
        self.start_system_scan()

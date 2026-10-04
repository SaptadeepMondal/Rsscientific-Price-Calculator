import customtkinter as ctk
from tkinter import messagebox
from app.data.db import get_loaded_files, remove_file_data

class ManageListsWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Manage Price Lists")
        self.geometry("600x400")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.title_label = ctk.CTkLabel(self, text="Loaded Price Lists", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(20, 10))
        
        # Scrollable frame for lists
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        
        self.refresh_list()
        
    def refresh_list(self):
        # Clear existing
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        files = get_loaded_files()
        
        if not files:
            empty_lbl = ctk.CTkLabel(self.scroll_frame, text="No price lists loaded yet.", text_color="gray")
            empty_lbl.grid(row=0, column=0, pady=20)
            return
            
        for i, file_info in enumerate(files):
            frame = ctk.CTkFrame(self.scroll_frame, fg_color="gray20", corner_radius=8)
            frame.grid(row=i, column=0, sticky="ew", pady=5)
            frame.grid_columnconfigure(0, weight=1)
            
            info_text = f"{file_info['source_file']} ({file_info['row_count']} products)\nLoaded on: {file_info['loaded_on']}"
            lbl = ctk.CTkLabel(frame, text=info_text, justify="left", anchor="w")
            lbl.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            
            btn = ctk.CTkButton(
                frame, 
                text="Remove", 
                fg_color="#D32F2F", 
                hover_color="#B71C1C", 
                width=80,
                command=lambda f=file_info['source_file']: self.remove_file(f)
            )
            btn.grid(row=0, column=1, padx=10, pady=10)
            
    def remove_file(self, filename):
        if messagebox.askyesno("Confirm", f"Are you sure you want to remove all data for '{filename}'?"):
            remove_file_data(filename)
            self.refresh_list()
            # If we need to trigger a refresh on the main window later, we can do it here.

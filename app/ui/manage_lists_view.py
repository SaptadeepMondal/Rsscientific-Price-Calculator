import customtkinter as ctk
from tkinter import messagebox
from app.data.db import get_loaded_files, remove_file_data
from app.ui.theme import *

class ManageListsWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Manage Price Lists")
        self.geometry("600x400")
        
        self.configure(fg_color=PANEL_GLASS)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.title_label = ctk.CTkLabel(self, text="Loaded Price Lists", font=get_font("header"), text_color=INK)
        self.title_label.grid(row=0, column=0, pady=(24, 12), padx=24, sticky="w")
        
        # Scrollable frame for lists
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 24))
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        
        self.refresh_list()
        
    def refresh_list(self):
        # Clear existing
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        files = get_loaded_files()
        
        if not files:
            empty_lbl = ctk.CTkLabel(self.scroll_frame, text="No price lists loaded yet.", font=get_font("body"), text_color=INK_MUTED)
            empty_lbl.grid(row=0, column=0, pady=40)
            return
            
        for i, file_info in enumerate(files):
            # A simple frame for layout
            row_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            row_frame.grid(row=i*2, column=0, sticky="ew", pady=12, padx=12)
            row_frame.grid_columnconfigure(0, weight=1)
            
            # Left: Details
            info_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            info_frame.grid(row=0, column=0, sticky="w")
            
            name_lbl = ctk.CTkLabel(info_frame, text=file_info['source_file'], font=get_font("body"), text_color=INK)
            name_lbl.grid(row=0, column=0, sticky="w")
            
            meta_text = f"{file_info['row_count']} products · Loaded on {file_info['loaded_on']}"
            meta_lbl = ctk.CTkLabel(info_frame, text=meta_text, font=get_font("metadata"), text_color=INK_MUTED)
            meta_lbl.grid(row=1, column=0, sticky="w")
            
            # Right: Remove
            btn = ctk.CTkButton(
                row_frame, 
                text="Remove", font=get_font("body"),
                fg_color="transparent", 
                text_color=REMOVE,
                hover_color=CANVAS,
                border_width=1, border_color=PANEL_EDGE,
                width=80, corner_radius=RAD_BUTTON,
                command=lambda f=file_info['source_file']: self.remove_file(f)
            )
            btn.grid(row=0, column=1, padx=(12, 0))
            
            # Hairline Divider
            divider = ctk.CTkFrame(self.scroll_frame, fg_color=PANEL_EDGE, height=1, corner_radius=0)
            divider.grid(row=i*2+1, column=0, sticky="ew")
            
    def remove_file(self, filename):
        if messagebox.askyesno("Confirm", f"Are you sure you want to remove all data for '{filename}'?"):
            remove_file_data(filename)
            self.refresh_list()

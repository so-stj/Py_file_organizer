#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Separation Destination Dialog
Simple dialog for selecting separation destination
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional
from pathlib import Path


class SeparationDestinationDialog:
    """Simple dialog for selecting separation destination"""
    
    def __init__(self, parent, config_manager, current_target: str = ""):
        self.parent = parent
        self.config_manager = config_manager
        self.current_target = current_target
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(self.config_manager.get_text("select_destination"))
        self.dialog.geometry("600x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)
        
        # Center dialog on parent
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (520 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (250 // 2)
        self.dialog.geometry(f"520x250+{x}+{y}")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create dialog widgets"""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text=self.config_manager.get_text("select_destination"), font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 25))
        
        # Select existing folder
        folder_frame = ttk.LabelFrame(main_frame, text=self.config_manager.get_text("select_existing_folder"), padding="15")
        folder_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 25))
        
        self.existing_folder_var = tk.StringVar()
        existing_folder_entry = ttk.Entry(folder_frame, textvariable=self.existing_folder_var, width=50, font=("Arial", 10))
        existing_folder_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 8))
        
        browse_button = ttk.Button(folder_frame, text=self.config_manager.get_text("browse"), 
                                  command=self.browse_folder, style="Accent.TButton")
        browse_button.grid(row=0, column=1, padx=(15, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(25, 0))
        
        ok_button = ttk.Button(button_frame, text="OK", command=self.on_ok, style="Accent.TButton", width=12)
        ok_button.grid(row=0, column=0, padx=(0, 15))
        
        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.on_cancel, width=12)
        cancel_button.grid(row=0, column=1)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        folder_frame.columnconfigure(0, weight=1)
        
        # Bind events
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)
        existing_folder_entry.focus()
    
    def browse_folder(self):
        """Browse for existing folder"""
        folder_path = filedialog.askdirectory(
            title=self.config_manager.get_text("select_existing_folder"),
            initialdir=self.current_target if self.current_target else "~"
        )
        
        if folder_path:
            self.existing_folder_var.set(folder_path)
    
    def validate_input(self) -> tuple[bool, str]:
        """Validate user input"""
        existing_folder = self.existing_folder_var.get().strip()
        
        # Check if folder is selected
        if not existing_folder:
            return False, self.config_manager.get_text("destination_path_required")
        
        # Validate existing folder
        if not Path(existing_folder).exists():
            return False, f"{self.config_manager.get_text('folder_not_exists')}: {existing_folder}"
        
        return True, ""
    
    def get_result(self) -> dict:
        """Get dialog result"""
        existing_folder = self.existing_folder_var.get().strip()
        
        if existing_folder:
            return {
                'type': 'existing',
                'path': existing_folder
            }
        
        return {}
    
    def on_ok(self):
        """Handle OK button click"""
        # Validate input
        is_valid, error_message = self.validate_input()
        if not is_valid:
            messagebox.showerror("Error", error_message)
            return
        
        # Get result
        self.result = self.get_result()
        
        # Close dialog
        self.dialog.destroy()
    
    def on_cancel(self):
        """Handle Cancel button click or window close"""
        self.result = None
        self.dialog.destroy()
    
    def show(self) -> Optional[dict]:
        """Show dialog and return result"""
        self.dialog.wait_window()
        return self.result

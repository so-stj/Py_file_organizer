#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Type Dialog
Responsible for adding and editing file type categories
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Tuple, Optional, List


class FileTypeDialog:
    """Dialog for adding or editing file type categories"""
    
    def __init__(self, parent, config_manager, title: str, category: str = "", extensions: Optional[List[str]] = None):
        self.parent = parent
        self.config_manager = config_manager
        self.title = title
        self.category = category
        self.extensions = extensions or []
        self.result = None
        
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("400x300")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_ui()
        self.window.wait_window()
    
    def setup_ui(self):
        """Build dialog UI"""
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Category name
        ttk.Label(main_frame, text=self.config_manager.get_text("category_name")).pack(anchor=tk.W)
        self.category_var = tk.StringVar(value=self.category)
        category_entry = ttk.Entry(main_frame, textvariable=self.category_var, width=40)
        category_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Extensions list
        ttk.Label(main_frame, text=self.config_manager.get_text("extensions_comma_separated")).pack(anchor=tk.W)
        
        extensions_text = scrolledtext.ScrolledText(main_frame, height=10, width=40)
        extensions_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        extensions_text.insert(1.0, ", ".join(self.extensions))
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="OK", 
                  command=lambda: self.save(extensions_text)).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(btn_frame, text="Cancel", 
                  command=self.window.destroy).pack(side=tk.RIGHT)
    
    def save(self, extensions_text):
        """Save the file type settings"""
        category = self.category_var.get().strip()
        if not category:
            messagebox.showerror("Error", self.config_manager.get_text("category_name_required"))
            return
        
        extensions_text_content = extensions_text.get(1.0, tk.END).strip()
        extensions = [ext.strip() for ext in extensions_text_content.split(",") if ext.strip()]
        
        if not extensions:
            messagebox.showerror("Error", self.config_manager.get_text("extensions_required"))
            return
        
        # Normalize extension format
        normalized_extensions = []
        for ext in extensions:
            if not ext.startswith("."):
                ext = "." + ext
            normalized_extensions.append(ext.lower())
        
        self.result = (category, normalized_extensions)
        self.window.destroy()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Language Selection Dialog
Responsible for displaying and handling language selection
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable


class LanguageSelectionDialog:
    """Dialog for selecting application language"""
    
    def __init__(self, parent, config_manager, on_language_selected: Optional[Callable] = None):
        self.parent = parent
        self.config_manager = config_manager
        self.on_language_selected = on_language_selected
        self.selected_language = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Language Selection / 言語選択")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)
        
        # Center the dialog
        self._center_dialog()
        
        self.setup_ui()
        self.dialog.wait_window()
    
    def _center_dialog(self):
        """Center the dialog on screen"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"400x300+{x}+{y}")
    
    def setup_ui(self):
        """Build the dialog UI"""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="Select your preferred language\nお好みの言語を選択してください", 
                               justify=tk.CENTER)
        title_label.pack(pady=(0, 20))
        
        # Language selection
        self.language_var = tk.StringVar(value=self.config_manager.current_language)
        
        # Japanese option
        ja_frame = ttk.Frame(main_frame)
        ja_frame.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(ja_frame, text="日本語", variable=self.language_var, 
                       value="ja").pack(side=tk.LEFT)
        ttk.Label(ja_frame, text="Japanese").pack(side=tk.LEFT, padx=(10, 0))
        
        # English option
        en_frame = ttk.Frame(main_frame)
        en_frame.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(en_frame, text="English", variable=self.language_var, 
                       value="en").pack(side=tk.LEFT)
        ttk.Label(en_frame, text="英語").pack(side=tk.LEFT, padx=(10, 0))
        
        # Swedish option
        sv_frame = ttk.Frame(main_frame)
        sv_frame.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(sv_frame, text="Svenska", variable=self.language_var, 
                       value="sv").pack(side=tk.LEFT)
        ttk.Label(sv_frame, text="スウェーデン語").pack(side=tk.LEFT, padx=(10, 0))
        
        # Description
        desc_label = ttk.Label(main_frame, 
                              text="You can change the language later in Settings.\n後で設定から言語を変更できます。", 
                              justify=tk.CENTER)
        desc_label.pack(pady=(20, 0))
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(btn_frame, text="OK / 決定", command=self._confirm_language).pack(side=tk.RIGHT)
    
    def _confirm_language(self):
        """Confirm language selection"""
        selected_language = self.language_var.get()
        self.selected_language = selected_language
        
        # Update config manager
        self.config_manager.change_language(selected_language)
        self.config_manager.set_setting("language_selected", True)
        
        # Call callback if provided
        if self.on_language_selected:
            self.on_language_selected(selected_language)
        
        self.dialog.destroy()
    
    def get_selected_language(self) -> Optional[str]:
        """Get the selected language"""
        return self.selected_language

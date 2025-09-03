#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings Window
Responsible for managing application settings UI
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Any, Optional
from .file_type_dialog import FileTypeDialog


class SettingsWindow:
    """Main settings window for the application"""
    
    def __init__(self, parent, config_manager, on_settings_changed: Optional[callable] = None):
        self.parent = parent
        self.config_manager = config_manager
        self.on_settings_changed = on_settings_changed
        
        self.window = tk.Toplevel(parent)
        self.window.geometry("600x500")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Set window title
        self.window.title(self.config_manager.get_text("settings"))
        
        self.setup_ui()
    
    def setup_ui(self):
        """Build settings UI"""
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # File type settings
        self.create_file_types_tab(notebook)
        
        # General settings
        self.create_general_tab(notebook)
        
        # Language settings
        self.create_language_tab(notebook)
        
        # Maintenance settings
        self.create_maintenance_tab(notebook)
    
    def create_file_types_tab(self, notebook):
        """Create file types settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=self.config_manager.get_text("file_types"))
        
        # File types list
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tree view
        columns = (self.config_manager.get_text("category"), self.config_manager.get_text("extensions"))
        self.tree = ttk.Treeview(list_frame, columns=columns, show="tree headings")
        self.tree.heading(self.config_manager.get_text("category"), text=self.config_manager.get_text("category"))
        self.tree.heading(self.config_manager.get_text("extensions"), text=self.config_manager.get_text("extensions"))
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Button frame
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(btn_frame, text=self.config_manager.get_text("add"), 
                  command=self.add_file_type).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text=self.config_manager.get_text("edit"), 
                  command=self.edit_file_type).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text=self.config_manager.get_text("delete"), 
                  command=self.delete_file_type).pack(side=tk.LEFT)
        
        self.load_file_types()
    
    def create_general_tab(self, notebook):
        """Create general settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=self.config_manager.get_text("general_settings"))
        
        # Settings options
        options_frame = ttk.LabelFrame(frame, text=self.config_manager.get_text("options"), padding="10")
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Auto organize
        self.auto_organize_var = tk.BooleanVar(value=self.config_manager.get_setting("auto_organize", True))
        ttk.Checkbutton(options_frame, text=self.config_manager.get_text("enable_auto_organize"), 
                       variable=self.auto_organize_var).pack(anchor=tk.W)
        
        # Create date folders
        self.create_date_folders_var = tk.BooleanVar(value=self.config_manager.get_setting("create_date_folders", True))
        ttk.Checkbutton(options_frame, text=self.config_manager.get_text("create_date_folders"), 
                       variable=self.create_date_folders_var).pack(anchor=tk.W)
        
        # Move duplicate files
        self.move_duplicates_var = tk.BooleanVar(value=self.config_manager.get_setting("move_duplicates", True))
        ttk.Checkbutton(options_frame, text=self.config_manager.get_text("auto_rename_duplicates"), 
                       variable=self.move_duplicates_var).pack(anchor=tk.W)
        
        # Save button
        ttk.Button(frame, text=self.config_manager.get_text("save"), 
                  command=self.save_settings).pack(pady=20)
    
    def create_language_tab(self, notebook):
        """Create language settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=self.config_manager.get_text("language"))
        
        # Language options
        lang_frame = ttk.LabelFrame(frame, text=self.config_manager.get_text("select_language"), padding="10")
        lang_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Language selection
        self.language_var = tk.StringVar(value=self.config_manager.get_setting("language", "ja"))
        
        ttk.Radiobutton(lang_frame, text=self.config_manager.get_text("japanese"), 
                       variable=self.language_var, value="ja").pack(anchor=tk.W)
        ttk.Radiobutton(lang_frame, text=self.config_manager.get_text("english"), 
                       variable=self.language_var, value="en").pack(anchor=tk.W)
        ttk.Radiobutton(lang_frame, text=self.config_manager.get_text("swedish"), 
                       variable=self.language_var, value="sv").pack(anchor=tk.W)
        
        # Save button
        ttk.Button(frame, text=self.config_manager.get_text("save"), 
                  command=self.save_language_settings).pack(pady=20)
    
    def create_maintenance_tab(self, notebook):
        """Create maintenance settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=self.config_manager.get_text("maintenance"))
        
        # Maintenance options
        maint_frame = ttk.LabelFrame(frame, text=self.config_manager.get_text("maintenance"), padding="10")
        maint_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Clear cache button
        ttk.Button(maint_frame, text=self.config_manager.get_text("clear_cache"), 
                  command=self.clear_cache).pack(anchor=tk.W, pady=5)
        
        # Reset to defaults button
        ttk.Button(maint_frame, text=self.config_manager.get_text("reset_to_defaults"), 
                  command=self.reset_to_defaults).pack(anchor=tk.W, pady=5)
        
        # Description
        desc_label = ttk.Label(frame, 
                              text=f"{self.config_manager.get_text('clear_cache_desc')}\n{self.config_manager.get_text('reset_defaults_desc')}", 
                              justify=tk.LEFT)
        desc_label.pack(pady=10)
    
    def load_file_types(self):
        """Load file types into tree view"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        file_types = self.config_manager.get_file_types()
        
        for category, extensions in file_types.items():
            item = self.tree.insert("", tk.END, text=category, values=(category, ", ".join(extensions)))
            for ext in extensions:
                self.tree.insert(item, tk.END, text=ext, values=("", ext))
    
    def add_file_type(self):
        """Add a new file type"""
        dialog = FileTypeDialog(self.window, self.config_manager, self.config_manager.get_text("new_file_type"))
        if dialog.result:
            category, extensions = dialog.result
            self.config_manager.add_file_type(category, extensions)
            self.load_file_types()
            self._notify_settings_changed()
    
    def edit_file_type(self):
        """Edit an existing file type"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", self.config_manager.get_text("warning_select_category"))
            return
        
        item = self.tree.item(selection[0])
        if item["text"] in self.config_manager.get_file_types():
            category = item["text"]
            extensions = self.config_manager.get_file_types()[category]
            
            dialog = FileTypeDialog(self.window, self.config_manager, 
                                  self.config_manager.get_text("edit_file_type"), 
                                  category, extensions)
            if dialog.result:
                new_category, new_extensions = dialog.result
                
                # Remove old category and add new one
                self.config_manager.remove_file_type(category)
                self.config_manager.add_file_type(new_category, new_extensions)
                
                self.load_file_types()
                self._notify_settings_changed()
    
    def delete_file_type(self):
        """Delete a file type"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", self.config_manager.get_text("warning_select_delete_category"))
            return
        
        item = self.tree.item(selection[0])
        category = item["text"]
        
        if messagebox.askyesno("Confirm", 
                              f"{self.config_manager.get_text('confirm_delete_category')} '{category}' {self.config_manager.get_text('confirm_delete_question')}"):
            self.config_manager.remove_file_type(category)
            self.load_file_types()
            self._notify_settings_changed()
    
    def save_settings(self):
        """Save general settings"""
        self.config_manager.set_setting("auto_organize", self.auto_organize_var.get())
        self.config_manager.set_setting("create_date_folders", self.create_date_folders_var.get())
        self.config_manager.set_setting("move_duplicates", self.move_duplicates_var.get())
        
        self.config_manager.save_config()
        self._notify_settings_changed()
        messagebox.showinfo("Complete", self.config_manager.get_text("settings_saved"))
        self.window.destroy()
    
    def save_language_settings(self):
        """Save language settings"""
        new_language = self.language_var.get()
        if new_language != self.config_manager.get_setting("language", "ja"):
            self.config_manager.change_language(new_language)
            self._notify_settings_changed()
            messagebox.showinfo("Info", self.config_manager.get_text("restart_required"))
        self.window.destroy()
    
    def clear_cache(self):
        """Clear cache (recent directories)"""
        if messagebox.askyesno("Confirm", self.config_manager.get_text("confirm_clear_cache")):
            self.config_manager.clear_recent_directories()
            self.config_manager.save_config()
            self._notify_settings_changed()
            messagebox.showinfo("Info", self.config_manager.get_text("cache_cleared"))
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        if messagebox.askyesno("Confirm", self.config_manager.get_text("confirm_reset_defaults")):
            self.config_manager.reset_to_defaults()
            self._notify_settings_changed()
            messagebox.showinfo("Info", self.config_manager.get_text("settings_reset"))
            self.window.destroy()
    
    def _notify_settings_changed(self):
        """Notify that settings have changed"""
        if self.on_settings_changed:
            self.on_settings_changed()

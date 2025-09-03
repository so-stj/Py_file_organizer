#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Application
Main application class that coordinates between different components
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from pathlib import Path
from typing import Optional

from config.config_manager import ConfigManager
from core.file_organizer_core import FileOrganizerCore
from utils.logger import Logger
from gui.language_dialog import LanguageSelectionDialog
from gui.settings_window import SettingsWindow


class FileOrganizerApp:
    """Main application class with separated responsibilities"""
    
    def __init__(self):
        print("Application initialization started")
        
        # Initialize components
        self.config_manager = self._setup_config_manager()
        self.file_organizer_core = FileOrganizerCore(self.config_manager)
        self.logger = Logger()
        
        # Initialize UI first
        self.root = tk.Tk()
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize variables after root window is created
        self.source_directory = tk.StringVar()
        self.target_directory = tk.StringVar()
        self.search_pattern = tk.StringVar()
        self.organizing = False
        
        # Check if this is first run and show language selection
        if not self.config_manager.get_setting("language_selected", False):
            print("First run: showing language selection dialog")
            self._show_language_selection()
        else:
            print("Using existing settings")
        
        # Set window title
        self.root.title(self.config_manager.get_text("app_title"))
        
        # Setup UI
        self.setup_ui()
        
        # Connect logger to UI
        self.logger.set_log_widget(self.log_text)
        
        print("Application initialization completed")
    
    def _setup_config_manager(self) -> ConfigManager:
        """Setup configuration manager with appropriate config file path"""
        if os.name == 'nt':  # Windows
            try:
                app_data_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'FileOrganizer')
                os.makedirs(app_data_dir, exist_ok=True)
                config_file = os.path.join(app_data_dir, "file_organizer_config.json")
                print(f"Windows config file path: {config_file}")
            except Exception as e:
                print(f"Windows config directory creation error: {e}")
                config_file = "file_organizer_config.json"
                print(f"Fallback config file path: {config_file}")
        else:  # Linux/Mac
            config_file = "file_organizer_config.json"
        
        print(f"Config file path: {config_file}")
        return ConfigManager(config_file)
    
    def _show_language_selection(self):
        """Show language selection dialog"""
        def on_language_selected(language: str):
            print(f"Language selected: {language}")
            self.root.title(self.config_manager.get_text("app_title"))
        
        LanguageSelectionDialog(self.root, self.config_manager, on_language_selected)
    
    def setup_ui(self):
        """Build main UI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Grid weight configuration
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text=self.config_manager.get_text("app_title"), 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Directory selection section
        self.create_directory_section(main_frame)
        
        # Control button section
        self.create_control_section(main_frame)
        
        # Search and separation section
        self.create_search_section(main_frame)
        
        # Log display area
        self.create_log_section(main_frame)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set(self.config_manager.get_text("ready"))
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def create_directory_section(self, parent):
        """Create directory selection section"""
        dir_frame = ttk.LabelFrame(parent, text=self.config_manager.get_text("directory_settings"), padding="10")
        dir_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        dir_frame.columnconfigure(1, weight=1)
        
        # Source directory
        ttk.Label(dir_frame, text=self.config_manager.get_text("source_directory")).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        source_entry = ttk.Entry(dir_frame, textvariable=self.source_directory, width=50)
        source_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(dir_frame, text=self.config_manager.get_text("browse"), command=self.browse_source).grid(row=0, column=2)
        
        # Target directory
        ttk.Label(dir_frame, text=self.config_manager.get_text("target_directory")).grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        target_entry = ttk.Entry(dir_frame, textvariable=self.target_directory, width=50)
        target_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        ttk.Button(dir_frame, text=self.config_manager.get_text("browse"), command=self.browse_target).grid(row=1, column=2, pady=(10, 0))
    
    def create_control_section(self, parent):
        """Create control button section"""
        control_frame = ttk.LabelFrame(parent, text=self.config_manager.get_text("operations"), padding="10")
        control_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Auto organize button
        self.organize_btn = ttk.Button(control_frame, text=self.config_manager.get_text("start_auto_organize"), 
                                      command=self.start_auto_organize)
        self.organize_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Stop button
        self.stop_btn = ttk.Button(control_frame, text=self.config_manager.get_text("stop"), 
                                  command=self.stop_organize, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Settings button
        ttk.Button(control_frame, text=self.config_manager.get_text("settings"), command=self.open_settings).grid(row=0, column=2, padx=(0, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, 
                                           maximum=100, length=300)
        self.progress_bar.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def create_search_section(self, parent):
        """Create search and separation section"""
        search_frame = ttk.LabelFrame(parent, text=self.config_manager.get_text("file_search_separation"), padding="10")
        search_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)
        
        # Search pattern
        ttk.Label(search_frame, text=self.config_manager.get_text("search_pattern")).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        search_entry = ttk.Entry(search_frame, textvariable=self.search_pattern, width=40)
        search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Search button
        ttk.Button(search_frame, text=self.config_manager.get_text("search"), command=self.search_files).grid(row=0, column=2, padx=(0, 10))
        
        # Separate button
        ttk.Button(search_frame, text=self.config_manager.get_text("separate_files"), command=self.separate_files).grid(row=0, column=3)
        
        # Search result display
        result_frame = ttk.Frame(search_frame)
        result_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        result_frame.columnconfigure(0, weight=1)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=6, width=80)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
    
    def create_log_section(self, parent):
        """Create log display section"""
        log_frame = ttk.LabelFrame(parent, text=self.config_manager.get_text("operation_log"), padding="10")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Log clear button
        ttk.Button(log_frame, text=self.config_manager.get_text("clear_log"), command=self.clear_log).grid(row=1, column=0, pady=(10, 0))
    
    def browse_source(self):
        """Select source directory"""
        directory = filedialog.askdirectory(title=self.config_manager.get_text("source_directory"))
        if directory:
            self.source_directory.set(directory)
            self.config_manager.add_recent_directory(directory)
            self.config_manager.save_config()
    
    def browse_target(self):
        """Select target directory"""
        directory = filedialog.askdirectory(title=self.config_manager.get_text("target_directory"))
        if directory:
            self.target_directory.set(directory)
            self.config_manager.add_recent_directory(directory)
            self.config_manager.save_config()
    
    def start_auto_organize(self):
        """Start auto organization"""
        # Validate directories
        is_valid, error_message = self.file_organizer_core.validate_directories(
            self.source_directory.get(), self.target_directory.get())
        
        if not is_valid:
            messagebox.showerror("Error", error_message)
            return
        
        if self.organizing:
            return
        
        self.organizing = True
        self.organize_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress_var.set(0)
        
        # Execute in separate thread
        thread = threading.Thread(target=self.auto_organize_files)
        thread.daemon = True
        thread.start()
    
    def stop_organize(self):
        """Stop organization"""
        self.organizing = False
        self.organize_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.logger.log_message(self.config_manager.get_text("organization_stopped"))
    
    def auto_organize_files(self):
        """Auto organize files"""
        try:
            source_path = Path(self.source_directory.get())
            target_path = Path(self.target_directory.get())
            
            # Create target directory
            target_path.mkdir(parents=True, exist_ok=True)
            
            # Get files
            files = self.file_organizer_core.get_files_for_organization(source_path)
            total_files = len(files)
            
            if total_files == 0:
                self.logger.log_message(self.config_manager.get_text("error_no_files_found"))
                return
            
            self.logger.log_message(f"{self.config_manager.get_text('start_organization')} {total_files} {self.config_manager.get_text('files_processed')}")
            
            processed = 0
            for file_path in files:
                if not self.organizing:
                    break
                
                success, message = self.file_organizer_core.organize_single_file(file_path, target_path)
                if success:
                    self.logger.log_message(message)
                else:
                    self.logger.log_error(message)
                
                processed += 1
                progress = (processed / total_files) * 100
                self.progress_var.set(progress)
                self.status_var.set(f"{self.config_manager.get_text('processing')}: {processed}/{total_files}")
            
            if self.organizing:
                self.logger.log_message(f"{self.config_manager.get_text('organization_complete_files')} {processed} {self.config_manager.get_text('files_processed_complete')}")
                self.status_var.set(self.config_manager.get_text("organization_complete"))
            else:
                self.logger.log_message(self.config_manager.get_text("organization_stopped"))
                
        except Exception as e:
            self.logger.log_error(f"Error: {e}")
        finally:
            self.organizing = False
            self.organize_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
    
    def search_files(self):
        """Search files"""
        # Validate source directory
        if not self.source_directory.get():
            messagebox.showerror("Error", self.config_manager.get_text("error_source_required"))
            return
        
        # Validate search pattern
        is_valid, error_message = self.file_organizer_core.validate_search_pattern(self.search_pattern.get())
        if not is_valid:
            messagebox.showerror("Error", error_message)
            return
        
        try:
            source_path = Path(self.source_directory.get())
            pattern = self.search_pattern.get()
            
            # Search files
            matching_files = self.file_organizer_core.search_files(source_path, pattern)
            
            # Display results
            self.result_text.delete(1.0, tk.END)
            if matching_files:
                self.result_text.insert(tk.END, f"{self.config_manager.get_text('search_results')} {len(matching_files)} {self.config_manager.get_text('files_found')}\n\n")
                for file_path in matching_files:
                    self.result_text.insert(tk.END, f"• {file_path.name}\n")
            else:
                self.result_text.insert(tk.END, self.config_manager.get_text("no_files_found"))
            
            self.logger.log_message(f"{self.config_manager.get_text('search_complete')} {self.config_manager.get_text('pattern_found')} '{pattern}' {len(matching_files)} {self.config_manager.get_text('files_discovered')}")
            
        except Exception as e:
            self.logger.log_error(f"{self.config_manager.get_text('search_error')} {e}")
    
    def separate_files(self):
        """Separate matching files"""
        # Validate target directory
        if not self.target_directory.get():
            messagebox.showerror("Error", self.config_manager.get_text("error_target_required"))
            return
        
        # Validate search pattern
        is_valid, error_message = self.file_organizer_core.validate_search_pattern(self.search_pattern.get())
        if not is_valid:
            messagebox.showerror("Error", error_message)
            return
        
        try:
            source_path = Path(self.source_directory.get())
            target_path = Path(self.target_directory.get())
            pattern = self.search_pattern.get()
            
            # Separate files
            moved_count, separate_path = self.file_organizer_core.separate_files(source_path, target_path, pattern)
            
            self.logger.log_message(f"{self.config_manager.get_text('separation_complete')} {moved_count} {self.config_manager.get_text('files_moved_to')} {separate_path.name} {self.config_manager.get_text('moved_to')}")
            messagebox.showinfo("Complete", f"{moved_count} {self.config_manager.get_text('files_separated')}\n{self.config_manager.get_text('save_location')} {separate_path}")
            
        except Exception as e:
            self.logger.log_error(f"{self.config_manager.get_text('separation_error')} {e}")
            messagebox.showerror("Error", f"{self.config_manager.get_text('separation_error_occurred')} {e}")
    
    def open_settings(self):
        """Open settings window"""
        def on_settings_changed():
            # Update UI elements that depend on settings
            self.root.title(self.config_manager.get_text("app_title"))
        
        SettingsWindow(self.root, self.config_manager, on_settings_changed)
    
    def clear_log(self):
        """Clear log"""
        self.logger.clear_log()
    
    def run(self):
        """Run application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = FileOrganizerApp()
    app.run()

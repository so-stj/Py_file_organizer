#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logger
Responsible for managing application logs and messages
"""

from datetime import datetime
from typing import List, Optional
import tkinter as tk
from tkinter import scrolledtext


class Logger:
    """Manages application logging and message display"""
    
    def __init__(self, log_widget: Optional[scrolledtext.ScrolledText] = None):
        self.log_widget = log_widget
        self.log_messages: List[str] = []
        self.max_messages = 1000  # Maximum number of messages to keep in memory
    
    def set_log_widget(self, log_widget: scrolledtext.ScrolledText) -> None:
        """Set the log widget for displaying messages"""
        self.log_widget = log_widget
    
    def log_message(self, message: str, show_timestamp: bool = True) -> None:
        """Add a log message with optional timestamp"""
        if show_timestamp:
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] {message}"
        else:
            formatted_message = message
        
        # Add to memory
        self.log_messages.append(formatted_message)
        
        # Limit memory usage
        if len(self.log_messages) > self.max_messages:
            self.log_messages = self.log_messages[-self.max_messages:]
        
        # Display in widget if available
        if self.log_widget:
            self.log_widget.insert(tk.END, formatted_message + "\n")
            self.log_widget.see(tk.END)
        
        # Also print to console
        print(formatted_message)
    
    def log_error(self, error_message: str) -> None:
        """Log an error message"""
        self.log_message(f"ERROR: {error_message}")
    
    def log_warning(self, warning_message: str) -> None:
        """Log a warning message"""
        self.log_message(f"WARNING: {warning_message}")
    
    def log_info(self, info_message: str) -> None:
        """Log an info message"""
        self.log_message(f"INFO: {info_message}")
    
    def clear_log(self) -> None:
        """Clear all log messages"""
        self.log_messages.clear()
        if self.log_widget:
            self.log_widget.delete(1.0, tk.END)
    
    def get_log_messages(self) -> List[str]:
        """Get all log messages"""
        return self.log_messages.copy()
    
    def get_recent_messages(self, count: int = 10) -> List[str]:
        """Get recent log messages"""
        return self.log_messages[-count:] if self.log_messages else []
    
    def export_log(self, file_path: str) -> bool:
        """Export log messages to a file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                for message in self.log_messages:
                    f.write(message + "\n")
            return True
        except Exception as e:
            self.log_error(f"Failed to export log: {e}")
            return False

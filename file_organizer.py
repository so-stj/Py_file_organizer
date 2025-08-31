#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Organization System
An application that automatically categorizes files and provides GUI operation
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import shutil
import re
from pathlib import Path
import json
from datetime import datetime
import threading
from typing import Dict, List, Tuple, Optional

class FileOrganizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Configuration file
        self.config_file = "file_organizer_config.json"
        
        # Setup language first
        self.setup_language()
        
        # Load config after language setup
        self.load_config()
        
        # Check if this is first run and show language selection
        if not self.config.get("language_selected", False):
            self.show_language_selection()
        
        # Update file types based on current language
        self.update_file_types_for_language()
        
        # Variables
        self.source_directory = tk.StringVar()
        self.target_directory = tk.StringVar()
        self.search_pattern = tk.StringVar()
        self.organizing = False
        
        # Set window title after language setup
        self.root.title(self.get_text("app_title"))
        
        self.setup_ui()
        self.load_recent_directories()
    
    def setup_language(self):
        """Setup language dictionaries"""
        # Initialize current language (will be updated after config load)
        self.current_language = "ja"
        
        # File type categories for different languages
        self.file_type_categories = {
            "ja": {
                "画像": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
                "動画": [".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv", ".webm"],
                "音声": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
                "文書": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
                "スプレッドシート": [".xls", ".xlsx", ".csv", ".ods"],
                "プレゼンテーション": [".ppt", ".pptx", ".odp"],
                "アーカイブ": [".zip", ".rar", ".7z", ".tar", ".gz"],
                "実行ファイル": [".exe", ".msi", ".dmg", ".deb", ".rpm"],
                "コード": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php"]
            },
            "en": {
                "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
                "Videos": [".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv", ".webm"],
                "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
                "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
                "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
                "Presentations": [".ppt", ".pptx", ".odp"],
                "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
                "Executables": [".exe", ".msi", ".dmg", ".deb", ".rpm"],
                "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php"]
            },
            "sv": {
                "Bilder": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
                "Videor": [".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv", ".webm"],
                "Ljud": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
                "Dokument": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
                "Kalkylblad": [".xls", ".xlsx", ".csv", ".ods"],
                "Presentationer": [".ppt", ".pptx", ".odp"],
                "Arkiv": [".zip", ".rar", ".7z", ".tar", ".gz"],
                "Körbara filer": [".exe", ".msi", ".dmg", ".deb", ".rpm"],
                "Kod": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php"]
            }
        }
        
        self.languages = {
            "ja": {
                "app_title": "ファイル仕分けシステム",
                "directory_settings": "ディレクトリ設定",
                "source_directory": "ソースディレクトリ:",
                "target_directory": "ターゲットディレクトリ:",
                "browse": "参照",
                "operations": "操作",
                "start_auto_organize": "自動仕分け開始",
                "stop": "停止",
                "settings": "設定",
                "file_search_separation": "ファイル検索・分離",
                "search_pattern": "検索パターン:",
                "search": "検索",
                "separate_files": "該当ファイルを分離",
                "operation_log": "操作ログ",
                "clear_log": "ログクリア",
                "ready": "準備完了",
                "processing": "処理中",
                "organization_complete": "仕分け完了",
                "organization_stopped": "仕分けが停止されました。",
                "error_source_target_required": "ソースディレクトリとターゲットディレクトリを指定してください。",
                "error_source_required": "ソースディレクトリを指定してください。",
                "error_target_required": "ターゲットディレクトリを指定してください。",
                "error_pattern_required": "検索パターンを入力してください。",
                "error_source_not_exists": "ソースディレクトリが存在しません:",
                "error_no_files_found": "仕分け対象のファイルが見つかりません。",
                "error_config_save": "設定保存エラー:",
                "start_organization": "仕分け開始:",
                "files_processed": "個のファイルを処理します...",
                "organization_complete_files": "仕分け完了:",
                "files_processed_complete": "個のファイルを処理しました。",
                "move_file": "移動:",
                "search_results": "検索結果:",
                "files_found": "個のファイルが見つかりました",
                "no_files_found": "該当するファイルが見つかりませんでした。",
                "search_complete": "検索完了:",
                "pattern_found": "パターン",
                "files_discovered": "個のファイルを発見",
                "search_error": "検索エラー:",
                "separation_complete": "分離完了:",
                "files_moved_to": "個のファイルを",
                "moved_to": "に移動しました。",
                "separation_error": "分離エラー:",
                "separation_error_occurred": "分離中にエラーが発生しました:",
                "files_separated": "個のファイルを分離しました。",
                "save_location": "保存先:",
                "warning_select_category": "編集するカテゴリを選択してください。",
                "warning_select_delete_category": "削除するカテゴリを選択してください。",
                "confirm_delete_category": "カテゴリ",
                "confirm_delete_question": "を削除しますか？",
                "settings_saved": "設定を保存しました。",
                "category_name": "カテゴリ名:",
                "category_name_required": "カテゴリ名を入力してください。",
                "extensions_comma_separated": "拡張子 (カンマ区切り):",
                "extensions_required": "拡張子を入力してください。",
                "new_file_type": "新しいファイルタイプ",
                "edit_file_type": "ファイルタイプを編集",
                "file_types": "ファイルタイプ",
                "general_settings": "一般設定",
                "options": "オプション",
                "enable_auto_organize": "自動仕分けを有効にする",
                "create_date_folders": "日付フォルダを作成する",
                "auto_rename_duplicates": "重複ファイルを自動的にリネームして移動",
                "save": "保存",
                "add": "追加",
                "edit": "編集",
                "delete": "削除",
                "category": "カテゴリ",
                "extensions": "拡張子",
                "language": "言語",
                "japanese": "日本語",
                "english": "English",
                "swedish": "Svenska",
                "select_language": "言語選択",
                "restart_required": "言語を変更するにはアプリケーションを再起動してください。",
                "other": "その他"
            },
            "en": {
                "app_title": "File Organization System",
                "directory_settings": "Directory Settings",
                "source_directory": "Source Directory:",
                "target_directory": "Target Directory:",
                "browse": "Browse",
                "operations": "Operations",
                "start_auto_organize": "Start Auto Organize",
                "stop": "Stop",
                "settings": "Settings",
                "file_search_separation": "File Search & Separation",
                "search_pattern": "Search Pattern:",
                "search": "Search",
                "separate_files": "Separate Matching Files",
                "operation_log": "Operation Log",
                "clear_log": "Clear Log",
                "ready": "Ready",
                "processing": "Processing",
                "organization_complete": "Organization Complete",
                "organization_stopped": "Organization stopped.",
                "error_source_target_required": "Please specify source and target directories.",
                "error_source_required": "Please specify source directory.",
                "error_target_required": "Please specify target directory.",
                "error_pattern_required": "Please enter search pattern.",
                "error_source_not_exists": "Source directory does not exist:",
                "error_no_files_found": "No files found for organization.",
                "error_config_save": "Config save error:",
                "start_organization": "Starting organization:",
                "files_processed": "files to process...",
                "organization_complete_files": "Organization complete:",
                "files_processed_complete": "files processed.",
                "move_file": "Move:",
                "search_results": "Search results:",
                "files_found": "files found",
                "no_files_found": "No matching files found.",
                "search_complete": "Search complete:",
                "pattern_found": "pattern",
                "files_discovered": "files discovered",
                "search_error": "Search error:",
                "separation_complete": "Separation complete:",
                "files_moved_to": "files moved to",
                "moved_to": ".",
                "separation_error": "Separation error:",
                "separation_error_occurred": "Error occurred during separation:",
                "files_separated": "files separated.",
                "save_location": "Save location:",
                "warning_select_category": "Please select a category to edit.",
                "warning_select_delete_category": "Please select a category to delete.",
                "confirm_delete_category": "Category",
                "confirm_delete_question": "will be deleted. Continue?",
                "settings_saved": "Settings saved.",
                "category_name": "Category Name:",
                "category_name_required": "Please enter category name.",
                "extensions_comma_separated": "Extensions (comma separated):",
                "extensions_required": "Please enter extensions.",
                "new_file_type": "New File Type",
                "edit_file_type": "Edit File Type",
                "file_types": "File Types",
                "general_settings": "General Settings",
                "options": "Options",
                "enable_auto_organize": "Enable auto organization",
                "create_date_folders": "Create date folders",
                "auto_rename_duplicates": "Auto rename and move duplicate files",
                "save": "Save",
                "add": "Add",
                "edit": "Edit",
                "delete": "Delete",
                "category": "Category",
                "extensions": "Extensions",
                "language": "Language",
                "japanese": "日本語",
                "english": "English",
                "swedish": "Svenska",
                "select_language": "Select Language",
                "restart_required": "Please restart the application to change language.",
                "other": "Other"
            },
            "sv": {
                "app_title": "Filorganiseringssystem",
                "directory_settings": "Kataloginställningar",
                "source_directory": "Källkatalog:",
                "target_directory": "Målkatalog:",
                "browse": "Bläddra",
                "operations": "Operationer",
                "start_auto_organize": "Starta automatisk organisering",
                "stop": "Stoppa",
                "settings": "Inställningar",
                "file_search_separation": "Filsökning & Separation",
                "search_pattern": "Sökmönster:",
                "search": "Sök",
                "separate_files": "Separera matchande filer",
                "operation_log": "Operationslogg",
                "clear_log": "Rensa logg",
                "ready": "Redo",
                "processing": "Bearbetar",
                "organization_complete": "Organisering slutförd",
                "organization_stopped": "Organisering stoppad.",
                "error_source_target_required": "Ange käll- och målkatalog.",
                "error_source_required": "Ange källkatalog.",
                "error_target_required": "Ange målkatalog.",
                "error_pattern_required": "Ange sökmönster.",
                "error_source_not_exists": "Källkatalog finns inte:",
                "error_no_files_found": "Inga filer hittades för organisering.",
                "error_config_save": "Konfigurationssparingsfel:",
                "start_organization": "Startar organisering:",
                "files_processed": "filer att bearbeta...",
                "organization_complete_files": "Organisering slutförd:",
                "files_processed_complete": "filer bearbetade.",
                "move_file": "Flytta:",
                "search_results": "Sökresultat:",
                "files_found": "filer hittade",
                "no_files_found": "Inga matchande filer hittades.",
                "search_complete": "Sökning slutförd:",
                "pattern_found": "mönster",
                "files_discovered": "filer upptäckta",
                "search_error": "Sökfel:",
                "separation_complete": "Separation slutförd:",
                "files_moved_to": "filer flyttade till",
                "moved_to": ".",
                "separation_error": "Separationsfel:",
                "separation_error_occurred": "Fel uppstod under separation:",
                "files_separated": "filer separerade.",
                "save_location": "Sparplats:",
                "warning_select_category": "Välj en kategori att redigera.",
                "warning_select_delete_category": "Välj en kategori att ta bort.",
                "confirm_delete_category": "Kategori",
                "confirm_delete_question": "kommer att tas bort. Fortsätt?",
                "settings_saved": "Inställningar sparade.",
                "category_name": "Kategorinamn:",
                "category_name_required": "Ange kategorinamn.",
                "extensions_comma_separated": "Filtillägg (kommaseparerade):",
                "extensions_required": "Ange filtillägg.",
                "new_file_type": "Ny filtyp",
                "edit_file_type": "Redigera filtyp",
                "file_types": "Filtyper",
                "general_settings": "Allmänna inställningar",
                "options": "Alternativ",
                "enable_auto_organize": "Aktivera automatisk organisering",
                "create_date_folders": "Skapa datummappar",
                "auto_rename_duplicates": "Byt namn och flytta duplicerade filer automatiskt",
                "save": "Spara",
                "add": "Lägg till",
                "edit": "Redigera",
                "delete": "Ta bort",
                "category": "Kategori",
                "extensions": "Filtillägg",
                "language": "Språk",
                "japanese": "日本語",
                "english": "English",
                "swedish": "Svenska",
                "select_language": "Välj språk",
                "restart_required": "Starta om applikationen för att ändra språk.",
                "other": "Övrigt"
            }
        }
    
    def get_text(self, key: str) -> str:
        """Get text in current language"""
        return self.languages.get(self.current_language, self.languages["ja"]).get(key, key)
    
    def change_language(self, language: str):
        """Change language"""
        if language in self.languages:
            self.current_language = language
            self.config["language"] = language
            self.update_file_types_for_language()
            self.save_config()
            messagebox.showinfo("Info", self.get_text("restart_required"))
    
    def show_language_selection(self):
        """Show language selection dialog on first run"""
        # Create language selection dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Language Selection / 言語選択")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")
        
        # Main frame
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Select your preferred language\nお好みの言語を選択してください", 
                               justify=tk.CENTER)
        title_label.pack(pady=(0, 20))
        
        # Language selection
        self.language_var = tk.StringVar(value=self.current_language)
        
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
        desc_label = ttk.Label(main_frame, text="You can change the language later in Settings.\n後で設定から言語を変更できます。", 
                              justify=tk.CENTER)
        desc_label.pack(pady=(20, 0))
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        def confirm_language():
            selected_language = self.language_var.get()
            self.current_language = selected_language
            self.config["language"] = selected_language
            self.config["language_selected"] = True
            self.save_config()
            dialog.destroy()
            # Update window title
            self.root.title(self.get_text("app_title"))
        
        ttk.Button(btn_frame, text="OK / 決定", command=confirm_language).pack(side=tk.RIGHT)
        
        # Make dialog modal
        dialog.wait_window()
    
    def update_file_types_for_language(self):
        """Update file types based on current language"""
        if self.current_language in self.file_type_categories:
            # Always update file types when language changes
            self.config["file_types"] = self.file_type_categories[self.current_language].copy()
    
    def load_config(self):
        """Load configuration file"""
        self.config = {
            "file_types": {},
            "recent_directories": [],
            "auto_organize": True,
            "create_date_folders": True,
            "move_duplicates": True,
            "language": "ja",
            "language_selected": False
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
            except:
                pass
        
        # Set current language from config
        self.current_language = self.config.get("language", "ja")
        
        # Update file types based on current language after loading config
        if self.current_language in self.file_type_categories:
            self.config["file_types"] = self.file_type_categories[self.current_language].copy()
    
    def save_config(self):
        """Save configuration file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"{self.get_text('error_config_save')} {e}")
    
    def setup_ui(self):
        """Build UI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Grid weight configuration
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text=self.get_text("app_title"), 
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
        self.status_var.set(self.get_text("ready"))
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def create_directory_section(self, parent):
        """Create directory selection section"""
        dir_frame = ttk.LabelFrame(parent, text=self.get_text("directory_settings"), padding="10")
        dir_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        dir_frame.columnconfigure(1, weight=1)
        
        # Source directory
        ttk.Label(dir_frame, text=self.get_text("source_directory")).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        source_entry = ttk.Entry(dir_frame, textvariable=self.source_directory, width=50)
        source_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(dir_frame, text=self.get_text("browse"), command=self.browse_source).grid(row=0, column=2)
        
        # Target directory
        ttk.Label(dir_frame, text=self.get_text("target_directory")).grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        target_entry = ttk.Entry(dir_frame, textvariable=self.target_directory, width=50)
        target_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        ttk.Button(dir_frame, text=self.get_text("browse"), command=self.browse_target).grid(row=1, column=2, pady=(10, 0))
    
    def create_control_section(self, parent):
        """Create control button section"""
        control_frame = ttk.LabelFrame(parent, text=self.get_text("operations"), padding="10")
        control_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Auto organize button
        self.organize_btn = ttk.Button(control_frame, text=self.get_text("start_auto_organize"), 
                                      command=self.start_auto_organize)
        self.organize_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Stop button
        self.stop_btn = ttk.Button(control_frame, text=self.get_text("stop"), 
                                  command=self.stop_organize, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Settings button
        ttk.Button(control_frame, text=self.get_text("settings"), command=self.open_settings).grid(row=0, column=2, padx=(0, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, 
                                           maximum=100, length=300)
        self.progress_bar.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def create_search_section(self, parent):
        """Create search and separation section"""
        search_frame = ttk.LabelFrame(parent, text=self.get_text("file_search_separation"), padding="10")
        search_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)
        
        # Search pattern
        ttk.Label(search_frame, text=self.get_text("search_pattern")).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        search_entry = ttk.Entry(search_frame, textvariable=self.search_pattern, width=40)
        search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Search button
        ttk.Button(search_frame, text=self.get_text("search"), command=self.search_files).grid(row=0, column=2, padx=(0, 10))
        
        # Separate button
        ttk.Button(search_frame, text=self.get_text("separate_files"), command=self.separate_files).grid(row=0, column=3)
        
        # Search result display
        result_frame = ttk.Frame(search_frame)
        result_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        result_frame.columnconfigure(0, weight=1)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=6, width=80)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
    
    def create_log_section(self, parent):
        """Create log display section"""
        log_frame = ttk.LabelFrame(parent, text=self.get_text("operation_log"), padding="10")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Log clear button
        ttk.Button(log_frame, text=self.get_text("clear_log"), command=self.clear_log).grid(row=1, column=0, pady=(10, 0))
    
    def browse_source(self):
        """Select source directory"""
        directory = filedialog.askdirectory(title=self.get_text("source_directory"))
        if directory:
            self.source_directory.set(directory)
            self.add_recent_directory(directory)
    
    def browse_target(self):
        """Select target directory"""
        directory = filedialog.askdirectory(title=self.get_text("target_directory"))
        if directory:
            self.target_directory.set(directory)
            self.add_recent_directory(directory)
    
    def add_recent_directory(self, directory):
        """Add to recently used directories"""
        if directory in self.config["recent_directories"]:
            self.config["recent_directories"].remove(directory)
        self.config["recent_directories"].insert(0, directory)
        self.config["recent_directories"] = self.config["recent_directories"][:10]
        self.save_config()
    
    def load_recent_directories(self):
        """Load recently used directories"""
        # Don't automatically set source directory on startup
        # Leave it empty for user to choose
        pass
    
    def start_auto_organize(self):
        """Start auto organization"""
        if not self.source_directory.get() or not self.target_directory.get():
            messagebox.showerror("Error", self.get_text("error_source_target_required"))
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
        self.log_message(self.get_text("organization_stopped"))
    
    def auto_organize_files(self):
        """Auto organize files"""
        try:
            source_path = Path(self.source_directory.get())
            target_path = Path(self.target_directory.get())
            
            if not source_path.exists():
                self.log_message(f"{self.get_text('error_source_not_exists')} {source_path}")
                return
            
            # Create target directory
            target_path.mkdir(parents=True, exist_ok=True)
            
            # Get files
            files = [f for f in source_path.iterdir() if f.is_file()]
            total_files = len(files)
            
            if total_files == 0:
                self.log_message(self.get_text("error_no_files_found"))
                return
            
            self.log_message(f"{self.get_text('start_organization')} {total_files} {self.get_text('files_processed')}")
            
            processed = 0
            for file_path in files:
                if not self.organizing:
                    break
                
                try:
                    self.organize_single_file(file_path, target_path)
                    processed += 1
                    progress = (processed / total_files) * 100
                    self.progress_var.set(progress)
                    self.status_var.set(f"{self.get_text('processing')}: {processed}/{total_files}")
                    
                except Exception as e:
                    self.log_message(f"Error ({file_path.name}): {e}")
            
            if self.organizing:
                self.log_message(f"{self.get_text('organization_complete_files')} {processed} {self.get_text('files_processed_complete')}")
                self.status_var.set(self.get_text("organization_complete"))
            else:
                self.log_message(self.get_text("organization_stopped"))
                
        except Exception as e:
            self.log_message(f"Error: {e}")
        finally:
            self.organizing = False
            self.organize_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
    
    def organize_single_file(self, file_path: Path, target_path: Path):
        """Organize single file"""
        file_extension = file_path.suffix.lower()
        
        # Determine file type
        category = self.get_text("other")
        for cat, extensions in self.config["file_types"].items():
            if file_extension in extensions:
                category = cat
                break
        
        # Create category directory
        category_path = target_path / category
        category_path.mkdir(exist_ok=True)
        
        # Create date folder (if setting is enabled)
        if self.config["create_date_folders"]:
            file_date = datetime.fromtimestamp(file_path.stat().st_mtime)
            date_folder = file_date.strftime("%Y-%m")
            category_path = category_path / date_folder
            category_path.mkdir(exist_ok=True)
        
        # Move file
        destination = category_path / file_path.name
        
        # Duplicate check
        if destination.exists() and self.config["move_duplicates"]:
            base_name = file_path.stem
            counter = 1
            while destination.exists():
                new_name = f"{base_name}_{counter}{file_extension}"
                destination = category_path / new_name
                counter += 1
        
        shutil.move(str(file_path), str(destination))
        self.log_message(f"{self.get_text('move_file')} {file_path.name} → {category}/{destination.name}")
    
    def search_files(self):
        """Search files"""
        if not self.source_directory.get():
            messagebox.showerror("Error", self.get_text("error_source_required"))
            return
        
        pattern = self.search_pattern.get()
        if not pattern:
            messagebox.showerror("Error", self.get_text("error_pattern_required"))
            return
        
        try:
            source_path = Path(self.source_directory.get())
            matching_files = []
            
            # Search files
            for file_path in source_path.rglob("*"):
                if file_path.is_file():
                    if re.search(pattern, file_path.name, re.IGNORECASE):
                        matching_files.append(file_path)
            
            # Display results
            self.result_text.delete(1.0, tk.END)
            if matching_files:
                self.result_text.insert(tk.END, f"{self.get_text('search_results')} {len(matching_files)} {self.get_text('files_found')}\n\n")
                for file_path in matching_files:
                    self.result_text.insert(tk.END, f"• {file_path.name}\n")
            else:
                self.result_text.insert(tk.END, self.get_text("no_files_found"))
            
            self.log_message(f"{self.get_text('search_complete')} {self.get_text('pattern_found')} '{pattern}' {len(matching_files)} {self.get_text('files_discovered')}")
            
        except Exception as e:
            self.log_message(f"{self.get_text('search_error')} {e}")
    
    def separate_files(self):
        """Separate matching files"""
        if not self.target_directory.get():
            messagebox.showerror("Error", self.get_text("error_target_required"))
            return
        
        pattern = self.search_pattern.get()
        if not pattern:
            messagebox.showerror("Error", self.get_text("error_pattern_required"))
            return
        
        try:
            source_path = Path(self.source_directory.get())
            target_path = Path(self.target_directory.get())
            
            # Create separation directory
            separate_path = target_path / f"分離_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            separate_path.mkdir(parents=True, exist_ok=True)
            
            moved_count = 0
            for file_path in source_path.rglob("*"):
                if file_path.is_file():
                    if re.search(pattern, file_path.name, re.IGNORECASE):
                        destination = separate_path / file_path.name
                        
                        # Duplicate check
                        if destination.exists():
                            base_name = file_path.stem
                            counter = 1
                            while destination.exists():
                                new_name = f"{base_name}_{counter}{file_path.suffix}"
                                destination = separate_path / new_name
                                counter += 1
                        
                        shutil.move(str(file_path), str(destination))
                        moved_count += 1
            
            self.log_message(f"{self.get_text('separation_complete')} {moved_count} {self.get_text('files_moved_to')} {separate_path.name} {self.get_text('moved_to')}")
            messagebox.showinfo("Complete", f"{moved_count} {self.get_text('files_separated')}\n{self.get_text('save_location')} {separate_path}")
            
        except Exception as e:
            self.log_message(f"{self.get_text('separation_error')} {e}")
            messagebox.showerror("Error", f"{self.get_text('separation_error_occurred')} {e}")
    
    def open_settings(self):
        """Open settings window"""
        SettingsWindow(self.root, self.config, self.save_config, self)
    
    def log_message(self, message: str):
        """Add log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        print(log_entry.strip())
    
    def clear_log(self):
        """Clear log"""
        self.log_text.delete(1.0, tk.END)
    
    def run(self):
        """Run application"""
        self.root.mainloop()


class SettingsWindow:
    def __init__(self, parent, config, save_callback, app_instance=None):
        self.window = tk.Toplevel(parent)
        self.window.geometry("600x500")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.config = config
        self.save_callback = save_callback
        self.app_instance = app_instance
        
        # Get current language from app instance
        self.current_language = app_instance.current_language if app_instance else "ja"
        self.languages = app_instance.languages if app_instance else {}
        
        # Set window title after language setup
        self.window.title(self.get_text("settings"))
        
        self.setup_ui()
    
    def get_text(self, key: str) -> str:
        """Get text in current language"""
        return self.languages.get(self.current_language, {}).get(key, key)
    
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
    
    def create_file_types_tab(self, notebook):
        """Create file types settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=self.get_text("file_types"))
        
        # File types list
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tree view
        columns = (self.get_text("category"), self.get_text("extensions"))
        self.tree = ttk.Treeview(list_frame, columns=columns, show="tree headings")
        self.tree.heading(self.get_text("category"), text=self.get_text("category"))
        self.tree.heading(self.get_text("extensions"), text=self.get_text("extensions"))
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Button frame
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(btn_frame, text=self.get_text("add"), command=self.add_file_type).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text=self.get_text("edit"), command=self.edit_file_type).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text=self.get_text("delete"), command=self.delete_file_type).pack(side=tk.LEFT)
        
        self.load_file_types()
    
    def create_general_tab(self, notebook):
        """Create general settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=self.get_text("general_settings"))
        
        # Settings options
        options_frame = ttk.LabelFrame(frame, text=self.get_text("options"), padding="10")
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Auto organize
        self.auto_organize_var = tk.BooleanVar(value=self.config["auto_organize"])
        ttk.Checkbutton(options_frame, text=self.get_text("enable_auto_organize"), 
                       variable=self.auto_organize_var).pack(anchor=tk.W)
        
        # Create date folders
        self.create_date_folders_var = tk.BooleanVar(value=self.config["create_date_folders"])
        ttk.Checkbutton(options_frame, text=self.get_text("create_date_folders"), 
                       variable=self.create_date_folders_var).pack(anchor=tk.W)
        
        # Move duplicate files
        self.move_duplicates_var = tk.BooleanVar(value=self.config["move_duplicates"])
        ttk.Checkbutton(options_frame, text=self.get_text("auto_rename_duplicates"), 
                       variable=self.move_duplicates_var).pack(anchor=tk.W)
        
        # Save button
        ttk.Button(frame, text=self.get_text("save"), command=self.save_settings).pack(pady=20)
    
    def create_language_tab(self, notebook):
        """Create language settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=self.get_text("language"))
        
        # Language options
        lang_frame = ttk.LabelFrame(frame, text=self.get_text("select_language"), padding="10")
        lang_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Language selection
        self.language_var = tk.StringVar(value=self.config.get("language", "ja"))
        
        ttk.Radiobutton(lang_frame, text=self.get_text("japanese"), variable=self.language_var, 
                       value="ja").pack(anchor=tk.W)
        ttk.Radiobutton(lang_frame, text=self.get_text("english"), variable=self.language_var, 
                       value="en").pack(anchor=tk.W)
        ttk.Radiobutton(lang_frame, text=self.get_text("swedish"), variable=self.language_var, 
                       value="sv").pack(anchor=tk.W)
        
        # Save button
        ttk.Button(frame, text=self.get_text("save"), command=self.save_language_settings).pack(pady=(20, 10))
        
        # Reset language selection button
        ttk.Button(frame, text="Reset Language Selection / 言語選択をリセット", 
                  command=self.reset_language_selection).pack(pady=(0, 20))
    
    def load_file_types(self):
        """Load file types into tree view"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get current file types from app instance if available
        file_types = self.config["file_types"]
        if self.app_instance and self.app_instance.current_language in self.app_instance.file_type_categories:
            file_types = self.app_instance.file_type_categories[self.app_instance.current_language]
        
        for category, extensions in file_types.items():
            item = self.tree.insert("", tk.END, text=category, values=(category, ", ".join(extensions)))
            for ext in extensions:
                self.tree.insert(item, tk.END, text=ext, values=("", ext))
    
    def add_file_type(self):
        """Add file type"""
        dialog = FileTypeDialog(self.window, self.get_text("new_file_type"), app_instance=self.app_instance)
        if dialog.result:
            category, extensions = dialog.result
            self.config["file_types"][category] = extensions
            # Also update the app instance file types
            if self.app_instance and self.app_instance.current_language in self.app_instance.file_type_categories:
                self.app_instance.file_type_categories[self.app_instance.current_language][category] = extensions
            self.load_file_types()
            # Save the configuration
            self.save_callback()
    
    def edit_file_type(self):
        """Edit file type"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", self.get_text("warning_select_category"))
            return
        
        item = self.tree.item(selection[0])
        if item["text"] in self.config["file_types"]:
            category = item["text"]
            extensions = self.config["file_types"][category]
            dialog = FileTypeDialog(self.window, self.get_text("edit_file_type"), category, extensions, app_instance=self.app_instance)
            if dialog.result:
                new_category, new_extensions = dialog.result
                if new_category != category:
                    del self.config["file_types"][category]
                self.config["file_types"][new_category] = new_extensions
                self.load_file_types()
    
    def delete_file_type(self):
        """Delete file type"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", self.get_text("warning_select_delete_category"))
            return
        
        item = self.tree.item(selection[0])
        category = item["text"]
        if category in self.config["file_types"]:
            if messagebox.askyesno("Confirm", f"{self.get_text('confirm_delete_category')} '{category}' {self.get_text('confirm_delete_question')}"):
                del self.config["file_types"][category]
                self.load_file_types()
    
    def save_settings(self):
        """Save settings"""
        self.config["auto_organize"] = self.auto_organize_var.get()
        self.config["create_date_folders"] = self.create_date_folders_var.get()
        self.config["move_duplicates"] = self.move_duplicates_var.get()
        
        self.save_callback()
        messagebox.showinfo("Complete", self.get_text("settings_saved"))
        self.window.destroy()
    
    def save_language_settings(self):
        """Save language settings"""
        new_language = self.language_var.get()
        if new_language != self.config.get("language", "ja"):
            self.config["language"] = new_language
            # Update file types for new language
            if self.app_instance and new_language in self.app_instance.file_type_categories:
                self.config["file_types"] = self.app_instance.file_type_categories[new_language].copy()
            self.save_callback()
            if self.app_instance:
                self.app_instance.change_language(new_language)
            else:
                messagebox.showinfo("Info", self.get_text("restart_required"))
        self.window.destroy()
    
    def reset_language_selection(self):
        """Reset language selection to show dialog on next startup"""
        if messagebox.askyesno("Confirm", "言語選択をリセットしますか？\n次回起動時に言語選択ダイアログが表示されます。\n\nReset language selection?\nLanguage selection dialog will appear on next startup."):
            self.config["language_selected"] = False
            self.save_callback()
            messagebox.showinfo("Info", "言語選択がリセットされました。\n次回起動時に言語選択ダイアログが表示されます。\n\nLanguage selection has been reset.\nLanguage selection dialog will appear on next startup.")


class FileTypeDialog:
    def __init__(self, parent, title, category="", extensions=None, app_instance=None):
        self.result = None
        
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("400x300")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Get language settings from parent
        self.current_language = "ja"
        self.languages = {}
        if hasattr(parent, 'master') and hasattr(parent.master, 'master'):
            # Try to get from main app
            main_app = parent.master.master
            if hasattr(main_app, 'current_language'):
                self.current_language = main_app.current_language
                self.languages = main_app.languages
        
        self.setup_ui(category, extensions or [])
        self.window.wait_window()
    
    def get_text(self, key: str) -> str:
        """Get text in current language"""
        return self.languages.get(self.current_language, {}).get(key, key)
    
    def setup_ui(self, category, extensions):
        """Build dialog UI"""
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Category name
        ttk.Label(main_frame, text=self.get_text("category_name")).pack(anchor=tk.W)
        self.category_var = tk.StringVar(value=category)
        category_entry = ttk.Entry(main_frame, textvariable=self.category_var, width=40)
        category_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Extensions list
        ttk.Label(main_frame, text=self.get_text("extensions_comma_separated")).pack(anchor=tk.W)
        
        extensions_text = scrolledtext.ScrolledText(main_frame, height=10, width=40)
        extensions_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        extensions_text.insert(1.0, ", ".join(extensions))
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="OK", command=lambda: self.save(extensions_text)).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(btn_frame, text="Cancel", command=self.window.destroy).pack(side=tk.RIGHT)
    
    def save(self, extensions_text):
        """Save settings"""
        category = self.category_var.get().strip()
        if not category:
            messagebox.showerror("Error", self.get_text("category_name_required"))
            return
        
        extensions_text_content = extensions_text.get(1.0, tk.END).strip()
        extensions = [ext.strip() for ext in extensions_text_content.split(",") if ext.strip()]
        
        if not extensions:
            messagebox.showerror("Error", self.get_text("extensions_required"))
            return
        
        # Normalize extension format
        normalized_extensions = []
        for ext in extensions:
            if not ext.startswith("."):
                ext = "." + ext
            normalized_extensions.append(ext.lower())
        
        self.result = (category, normalized_extensions)
        self.window.destroy()


if __name__ == "__main__":
    app = FileOrganizer()
    app.run()

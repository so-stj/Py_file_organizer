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
        self.root.title("ファイル仕分けシステム")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Configuration file
        self.config_file = "file_organizer_config.json"
        self.load_config()
        
        # Variables
        self.source_directory = tk.StringVar()
        self.target_directory = tk.StringVar()
        self.search_pattern = tk.StringVar()
        self.organizing = False
        
        self.setup_ui()
        self.load_recent_directories()
    
    def load_config(self):
        """Load configuration file"""
        self.config = {
            "file_types": {
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
            "recent_directories": [],
            "auto_organize": True,
            "create_date_folders": True,
            "move_duplicates": True
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
            except:
                pass
    
    def save_config(self):
        """Save configuration file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"設定保存エラー: {e}")
    
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
        title_label = ttk.Label(main_frame, text="ファイル仕分けシステム", 
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
        self.status_var.set("準備完了")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def create_directory_section(self, parent):
        """Create directory selection section"""
        dir_frame = ttk.LabelFrame(parent, text="ディレクトリ設定", padding="10")
        dir_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        dir_frame.columnconfigure(1, weight=1)
        
        # Source directory
        ttk.Label(dir_frame, text="ソースディレクトリ:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        source_entry = ttk.Entry(dir_frame, textvariable=self.source_directory, width=50)
        source_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(dir_frame, text="参照", command=self.browse_source).grid(row=0, column=2)
        
        # Target directory
        ttk.Label(dir_frame, text="ターゲットディレクトリ:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        target_entry = ttk.Entry(dir_frame, textvariable=self.target_directory, width=50)
        target_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        ttk.Button(dir_frame, text="参照", command=self.browse_target).grid(row=1, column=2, pady=(10, 0))
    
    def create_control_section(self, parent):
        """Create control button section"""
        control_frame = ttk.LabelFrame(parent, text="操作", padding="10")
        control_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Auto organize button
        self.organize_btn = ttk.Button(control_frame, text="自動仕分け開始", 
                                      command=self.start_auto_organize)
        self.organize_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Stop button
        self.stop_btn = ttk.Button(control_frame, text="停止", 
                                  command=self.stop_organize, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Settings button
        ttk.Button(control_frame, text="設定", command=self.open_settings).grid(row=0, column=2, padx=(0, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, 
                                           maximum=100, length=300)
        self.progress_bar.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def create_search_section(self, parent):
        """Create search and separation section"""
        search_frame = ttk.LabelFrame(parent, text="ファイル検索・分離", padding="10")
        search_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)
        
        # Search pattern
        ttk.Label(search_frame, text="検索パターン:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        search_entry = ttk.Entry(search_frame, textvariable=self.search_pattern, width=40)
        search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Search button
        ttk.Button(search_frame, text="検索", command=self.search_files).grid(row=0, column=2, padx=(0, 10))
        
        # Separate button
        ttk.Button(search_frame, text="該当ファイルを分離", command=self.separate_files).grid(row=0, column=3)
        
        # Search result display
        result_frame = ttk.Frame(search_frame)
        result_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        result_frame.columnconfigure(0, weight=1)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=6, width=80)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
    
    def create_log_section(self, parent):
        """Create log display section"""
        log_frame = ttk.LabelFrame(parent, text="操作ログ", padding="10")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Log clear button
        ttk.Button(log_frame, text="ログクリア", command=self.clear_log).grid(row=1, column=0, pady=(10, 0))
    
    def browse_source(self):
        """Select source directory"""
        directory = filedialog.askdirectory(title="ソースディレクトリを選択")
        if directory:
            self.source_directory.set(directory)
            self.add_recent_directory(directory)
    
    def browse_target(self):
        """Select target directory"""
        directory = filedialog.askdirectory(title="ターゲットディレクトリを選択")
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
        if self.config["recent_directories"]:
            self.source_directory.set(self.config["recent_directories"][0])
    
    def start_auto_organize(self):
        """Start auto organization"""
        if not self.source_directory.get() or not self.target_directory.get():
            messagebox.showerror("エラー", "ソースディレクトリとターゲットディレクトリを指定してください。")
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
        self.log_message("仕分けを停止しました。")
    
    def auto_organize_files(self):
        """Auto organize files"""
        try:
            source_path = Path(self.source_directory.get())
            target_path = Path(self.target_directory.get())
            
            if not source_path.exists():
                self.log_message(f"エラー: ソースディレクトリが存在しません: {source_path}")
                return
            
            # Create target directory
            target_path.mkdir(parents=True, exist_ok=True)
            
            # Get files
            files = [f for f in source_path.iterdir() if f.is_file()]
            total_files = len(files)
            
            if total_files == 0:
                self.log_message("仕分け対象のファイルが見つかりません。")
                return
            
            self.log_message(f"仕分け開始: {total_files}個のファイルを処理します...")
            
            processed = 0
            for file_path in files:
                if not self.organizing:
                    break
                
                try:
                    self.organize_single_file(file_path, target_path)
                    processed += 1
                    progress = (processed / total_files) * 100
                    self.progress_var.set(progress)
                    self.status_var.set(f"処理中: {processed}/{total_files}")
                    
                except Exception as e:
                    self.log_message(f"エラー ({file_path.name}): {e}")
            
            if self.organizing:
                self.log_message(f"仕分け完了: {processed}個のファイルを処理しました。")
                self.status_var.set("仕分け完了")
            else:
                self.log_message("仕分けが停止されました。")
                
        except Exception as e:
            self.log_message(f"エラー: {e}")
        finally:
            self.organizing = False
            self.organize_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
    
    def organize_single_file(self, file_path: Path, target_path: Path):
        """Organize single file"""
        file_extension = file_path.suffix.lower()
        
        # Determine file type
        category = "その他"
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
        self.log_message(f"移動: {file_path.name} → {category}/{destination.name}")
    
    def search_files(self):
        """Search files"""
        if not self.source_directory.get():
            messagebox.showerror("エラー", "ソースディレクトリを指定してください。")
            return
        
        pattern = self.search_pattern.get()
        if not pattern:
            messagebox.showerror("エラー", "検索パターンを入力してください。")
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
                self.result_text.insert(tk.END, f"検索結果: {len(matching_files)}個のファイルが見つかりました\n\n")
                for file_path in matching_files:
                    self.result_text.insert(tk.END, f"• {file_path.name}\n")
            else:
                self.result_text.insert(tk.END, "該当するファイルが見つかりませんでした。")
            
            self.log_message(f"検索完了: パターン '{pattern}' で {len(matching_files)}個のファイルを発見")
            
        except Exception as e:
            self.log_message(f"検索エラー: {e}")
    
    def separate_files(self):
        """Separate matching files"""
        if not self.target_directory.get():
            messagebox.showerror("エラー", "ターゲットディレクトリを指定してください。")
            return
        
        pattern = self.search_pattern.get()
        if not pattern:
            messagebox.showerror("エラー", "検索パターンを入力してください。")
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
            
            self.log_message(f"分離完了: {moved_count}個のファイルを {separate_path.name} に移動しました。")
            messagebox.showinfo("完了", f"{moved_count}個のファイルを分離しました。\n保存先: {separate_path}")
            
        except Exception as e:
            self.log_message(f"分離エラー: {e}")
            messagebox.showerror("エラー", f"分離中にエラーが発生しました: {e}")
    
    def open_settings(self):
        """Open settings window"""
        SettingsWindow(self.root, self.config, self.save_config)
    
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
    def __init__(self, parent, config, save_callback):
        self.window = tk.Toplevel(parent)
        self.window.title("設定")
        self.window.geometry("600x500")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.config = config
        self.save_callback = save_callback
        
        self.setup_ui()
    
    def setup_ui(self):
        """Build settings UI"""
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # File type settings
        self.create_file_types_tab(notebook)
        
        # General settings
        self.create_general_tab(notebook)
    
    def create_file_types_tab(self, notebook):
        """Create file types settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="ファイルタイプ")
        
        # File types list
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tree view
        columns = ("カテゴリ", "拡張子")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="tree headings")
        self.tree.heading("カテゴリ", text="カテゴリ")
        self.tree.heading("拡張子", text="拡張子")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Button frame
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(btn_frame, text="追加", command=self.add_file_type).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="編集", command=self.edit_file_type).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="削除", command=self.delete_file_type).pack(side=tk.LEFT)
        
        self.load_file_types()
    
    def create_general_tab(self, notebook):
        """Create general settings tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="一般設定")
        
        # Settings options
        options_frame = ttk.LabelFrame(frame, text="オプション", padding="10")
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Auto organize
        self.auto_organize_var = tk.BooleanVar(value=self.config["auto_organize"])
        ttk.Checkbutton(options_frame, text="自動仕分けを有効にする", 
                       variable=self.auto_organize_var).pack(anchor=tk.W)
        
        # Create date folders
        self.create_date_folders_var = tk.BooleanVar(value=self.config["create_date_folders"])
        ttk.Checkbutton(options_frame, text="日付フォルダを作成する", 
                       variable=self.create_date_folders_var).pack(anchor=tk.W)
        
        # Move duplicate files
        self.move_duplicates_var = tk.BooleanVar(value=self.config["move_duplicates"])
        ttk.Checkbutton(options_frame, text="重複ファイルを自動的にリネームして移動", 
                       variable=self.move_duplicates_var).pack(anchor=tk.W)
        
        # Save button
        ttk.Button(frame, text="保存", command=self.save_settings).pack(pady=20)
    
    def load_file_types(self):
        """Load file types into tree view"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for category, extensions in self.config["file_types"].items():
            item = self.tree.insert("", tk.END, text=category, values=(category, ", ".join(extensions)))
            for ext in extensions:
                self.tree.insert(item, tk.END, text=ext, values=("", ext))
    
    def add_file_type(self):
        """Add file type"""
        dialog = FileTypeDialog(self.window, "新しいファイルタイプ")
        if dialog.result:
            category, extensions = dialog.result
            self.config["file_types"][category] = extensions
            self.load_file_types()
    
    def edit_file_type(self):
        """Edit file type"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "編集するカテゴリを選択してください。")
            return
        
        item = self.tree.item(selection[0])
        if item["text"] in self.config["file_types"]:
            category = item["text"]
            extensions = self.config["file_types"][category]
            dialog = FileTypeDialog(self.window, "ファイルタイプを編集", category, extensions)
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
            messagebox.showwarning("警告", "削除するカテゴリを選択してください。")
            return
        
        item = self.tree.item(selection[0])
        category = item["text"]
        if category in self.config["file_types"]:
            if messagebox.askyesno("確認", f"カテゴリ '{category}' を削除しますか？"):
                del self.config["file_types"][category]
                self.load_file_types()
    
    def save_settings(self):
        """Save settings"""
        self.config["auto_organize"] = self.auto_organize_var.get()
        self.config["create_date_folders"] = self.create_date_folders_var.get()
        self.config["move_duplicates"] = self.move_duplicates_var.get()
        
        self.save_callback()
        messagebox.showinfo("完了", "設定を保存しました。")
        self.window.destroy()


class FileTypeDialog:
    def __init__(self, parent, title, category="", extensions=None):
        self.result = None
        
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("400x300")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_ui(category, extensions or [])
        self.window.wait_window()
    
    def setup_ui(self, category, extensions):
        """Build dialog UI"""
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Category name
        ttk.Label(main_frame, text="カテゴリ名:").pack(anchor=tk.W)
        self.category_var = tk.StringVar(value=category)
        category_entry = ttk.Entry(main_frame, textvariable=self.category_var, width=40)
        category_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Extensions list
        ttk.Label(main_frame, text="拡張子 (カンマ区切り):").pack(anchor=tk.W)
        
        extensions_text = scrolledtext.ScrolledText(main_frame, height=10, width=40)
        extensions_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        extensions_text.insert(1.0, ", ".join(extensions))
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="OK", command=lambda: self.save(extensions_text)).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(btn_frame, text="キャンセル", command=self.window.destroy).pack(side=tk.RIGHT)
    
    def save(self, extensions_text):
        """Save settings"""
        category = self.category_var.get().strip()
        if not category:
            messagebox.showerror("エラー", "カテゴリ名を入力してください。")
            return
        
        extensions_text_content = extensions_text.get(1.0, tk.END).strip()
        extensions = [ext.strip() for ext in extensions_text_content.split(",") if ext.strip()]
        
        if not extensions:
            messagebox.showerror("エラー", "拡張子を入力してください。")
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

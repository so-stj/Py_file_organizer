#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration Manager
Responsible for managing application configuration, language settings, and file type categories
"""

import os
import json
from typing import Dict, List, Any, Optional
from pathlib import Path


class ConfigManager:
    """Manages application configuration and settings"""
    
    def __init__(self, config_file: str = "file_organizer_config.json"):
        self.config_file = config_file
        self.config = self._get_default_config()
        self.current_language = "ja"
        self.languages = self._setup_languages()
        self.file_type_categories = self._setup_file_type_categories()
        
        # Load configuration
        self.load_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "file_types": {},
            "recent_directories": [],
            "auto_organize": True,
            "create_date_folders": True,
            "move_duplicates": True,
            "language": "ja",
            "language_selected": False,
            "deleted_default_categories": []
        }
    
    def _setup_languages(self) -> Dict[str, Dict[str, str]]:
        """Setup language dictionaries"""
        return {
            "ja": {
                "app_title": "ファイル自動整理アプリ",
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
                "maintenance": "メンテナンス",
                "clear_cache": "キャッシュクリア",
                "reset_to_defaults": "初期化",
                "reset_language_selection": "言語選択リセット",
                "clear_cache_desc": "キャッシュクリア: 最近使用したディレクトリをクリア",
                "reset_defaults_desc": "初期化: すべての設定をデフォルトに戻す",
                "reset_language_desc": "言語選択リセット: 次回起動時に言語選択ダイアログを表示",
                "confirm_clear_cache": "最近使用したディレクトリをクリアしますか？",
                "confirm_reset_defaults": "すべての設定を初期化しますか？\nこの操作は元に戻せません。",
                "cache_cleared": "キャッシュをクリアしました。",
                "settings_reset": "設定を初期化しました。\nアプリケーションを再起動してください。",
                "other": "その他"
            },
            "en": {
                "app_title": "File Organizer App",
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
                "maintenance": "Maintenance",
                "clear_cache": "Clear Cache",
                "reset_to_defaults": "Reset to Defaults",
                "reset_language_selection": "Reset Language Selection",
                "clear_cache_desc": "Clear Cache: Clear recent directories",
                "reset_defaults_desc": "Reset to Defaults: Reset all settings to defaults",
                "reset_language_desc": "Reset Language Selection: Show language selection dialog on next startup",
                "confirm_clear_cache": "Clear recent directories?",
                "confirm_reset_defaults": "Reset all settings to defaults?\nThis action cannot be undone.",
                "cache_cleared": "Cache cleared.",
                "settings_reset": "Settings reset to defaults.\nPlease restart the application.",
                "other": "Other"
            },
            "sv": {
                "app_title": "Filorganiseringsapp",
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
                "clear_cache": "Rensa cache",
                "reset_to_defaults": "Återställ till standard",
                "reset_language_selection": "Återställ språkval",
                "clear_cache_desc": "Rensa cache: Rensa nyligen använda kataloger",
                "reset_defaults_desc": "Återställ till standard: Återställ alla inställningar till standard",
                "reset_language_desc": "Återställ språkval: Visa språkvalsdialog vid nästa start",
                "confirm_clear_cache": "Rensa nyligen använda kataloger?",
                "confirm_reset_defaults": "Återställ alla inställningar till standard?\nDenna åtgärd kan inte ångras.",
                "cache_cleared": "Cache rensad.",
                "settings_reset": "Inställningar återställda till standard.\nStarta om applikationen.",
                "other": "Övrigt"
            }
        }
    
    def _setup_file_type_categories(self) -> Dict[str, Dict[str, List[str]]]:
        """Setup file type categories for different languages"""
        return {
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
    
    def get_text(self, key: str) -> str:
        """Get text in current language"""
        return self.languages.get(self.current_language, self.languages["ja"]).get(key, key)
    
    def change_language(self, language: str) -> None:
        """Change current language"""
        if language in self.languages:
            print(f"Changing language from '{self.current_language}' to '{language}'")
            
            # Get current file types before language change
            current_file_types = self.config.get("file_types", {}).copy()
            print(f"Current file types: {list(current_file_types.keys())}")
            
            # Identify custom categories (not in any default language)
            custom_categories = {}
            for category, extensions in current_file_types.items():
                is_default_in_any_language = False
                for lang in self.file_type_categories:
                    if category in self.file_type_categories[lang]:
                        is_default_in_any_language = True
                        print(f"  '{category}' is default in language '{lang}'")
                        break
                
                if not is_default_in_any_language:
                    custom_categories[category] = extensions
                    print(f"  '{category}' is CUSTOM category")
                else:
                    print(f"  '{category}' is DEFAULT category")
            
            print(f"Custom categories to preserve: {list(custom_categories.keys())}")
            
            # Update language
            self.current_language = language
            self.config["language"] = language
            
            # Get new language's default categories
            if language in self.file_type_categories:
                new_default_categories = self.file_type_categories[language].copy()
                print(f"New language '{language}' default categories: {list(new_default_categories.keys())}")
                
                # Get deleted default categories for new language
                deleted_defaults = self.config.get("deleted_default_categories", [])
                deleted_categories = set()
                
                for deletion_info in deleted_defaults:
                    if isinstance(deletion_info, dict):
                        deleted_category = deletion_info.get("category")
                        deleted_language = deletion_info.get("language")
                        deleted_extensions = deletion_info.get("extensions")
                        
                        # Check if this deletion applies to new language
                        if deleted_language == language:
                            deleted_categories.add(deleted_category)
                            print(f"  '{deleted_category}' is marked as deleted for new language")
                        else:
                            # Check if extensions match any category in new language
                            for new_category, new_extensions in new_default_categories.items():
                                if new_extensions == deleted_extensions:
                                    deleted_categories.add(new_category)
                                    print(f"  '{new_category}' is marked as deleted (equivalent to '{deleted_category}' from '{deleted_language}')")
                                    break
                    elif isinstance(deletion_info, str):
                        # Handle old string format
                        if deletion_info in new_default_categories:
                            deleted_categories.add(deletion_info)
                            print(f"  '{deletion_info}' is marked as deleted (old format)")
                
                print(f"Deleted categories for new language: {list(deleted_categories)}")
                
                # Merge new defaults with custom categories (excluding deleted ones)
                merged_categories = {}
                
                # Add new language defaults (excluding deleted ones)
                for category, extensions in new_default_categories.items():
                    if category not in deleted_categories:
                        merged_categories[category] = extensions
                        print(f"  Added default category: '{category}'")
                    else:
                        print(f"  Skipped deleted default category: '{category}'")
                
                # Add custom categories
                for category, extensions in custom_categories.items():
                    merged_categories[category] = extensions
                    print(f"  Added custom category: '{category}'")
                
                # Update config
                self.config["file_types"] = merged_categories
                print(f"Final merged categories: {list(merged_categories.keys())}")
                print(f"Config updated with merged categories")
                
                # Save configuration
                print(f"About to save config after language change...")
                self.save_config()
                print(f"Config saved after language change")
                
                # Verify the config was actually updated
                if self.config.get("file_types"):
                    print(f"✓ Config verification after language change:")
                    print(f"  - file_types count: {len(self.config['file_types'])}")
                    print(f"  - file_types keys: {list(self.config['file_types'].keys())}")
                else:
                    print(f"✗ ERROR: Config file_types is empty after language change!")
            else:
                print(f"Language '{language}' not found in file type categories")
        else:
            print(f"Language '{language}' not supported")
    
    def get_file_types(self) -> Dict[str, List[str]]:
        """Get current file types configuration"""
        return self.config.get("file_types", {})
    
    def set_file_types(self, file_types: Dict[str, List[str]]) -> None:
        """Set file types configuration"""
        self.config["file_types"] = file_types
    
    def add_file_type(self, category: str, extensions: List[str]) -> None:
        """Add a new file type category"""
        print(f"=== Adding custom category ===")
        print(f"Category: {category}")
        print(f"Extensions: {extensions}")
        print(f"Current language: {self.current_language}")
        
        # Check if this is a custom category
        is_default_in_any_language = False
        for lang in self.file_type_categories:
            if category in self.file_type_categories[lang]:
                is_default_in_any_language = True
                print(f"  WARNING: '{category}' already exists in default language '{lang}'")
                break
        
        if not is_default_in_any_language:
            print(f"  ✓ Confirmed as custom category")
        else:
            print(f"  ✗ This is a default category, not custom")
        
        # Add to config
        self.config["file_types"][category] = extensions
        print(f"  Added to config['file_types']: {list(self.config['file_types'].keys())}")
        
        # Save configuration immediately
        print(f"  About to save config...")
        self.save_config()
        print(f"  Config saved")
        
        # Verify the category was actually saved
        if category in self.config["file_types"]:
            print(f"  ✓ Category '{category}' successfully saved in config")
        else:
            print(f"  ✗ ERROR: Category '{category}' was NOT saved in config!")
        
        print(f"  Final categories count: {len(self.config['file_types'])}")
        print(f"  Final categories: {list(self.config['file_types'].keys())}")
    
    def remove_file_type(self, category: str) -> None:
        """Remove a file type category"""
        if category in self.config["file_types"]:
            print(f"=== Removing file type category ===")
            print(f"Category: {category}")
            
            # Check if this is a default category
            is_default_category = False
            for lang in self.file_type_categories:
                if category in self.file_type_categories[lang]:
                    is_default_category = True
                    print(f"  '{category}' is a default category in language '{lang}'")
                    
                    # Record this deletion to prevent it from being restored
                    if "deleted_default_categories" not in self.config:
                        self.config["deleted_default_categories"] = []
                    
                    deletion_info = {
                        "category": category,
                        "language": lang,
                        "extensions": self.file_type_categories[lang][category]
                    }
                    
                    # Check if already recorded
                    already_deleted = False
                    for existing_deletion in self.config["deleted_default_categories"]:
                        if (isinstance(existing_deletion, dict) and 
                            existing_deletion.get("category") == category and
                            existing_deletion.get("language") == lang):
                            already_deleted = True
                            break
                    
                    if not already_deleted:
                        self.config["deleted_default_categories"].append(deletion_info)
                        print(f"  Recorded deletion of default category '{category}' from '{lang}'")
                    else:
                        print(f"  Deletion already recorded for '{category}' from '{lang}'")
                    break
            
            if not is_default_category:
                print(f"  '{category}' is a custom category")
            
            # Remove from config
            del self.config["file_types"][category]
            print(f"  Removed '{category}' from config")
            
            # Save configuration immediately
            self.save_config()
            print(f"  Config saved after removal")
        else:
            print(f"Category '{category}' not found in config")
    
    def get_recent_directories(self) -> List[str]:
        """Get recent directories list"""
        return self.config.get("recent_directories", [])
    
    def add_recent_directory(self, directory: str) -> None:
        """Add directory to recent directories list"""
        if directory in self.config["recent_directories"]:
            self.config["recent_directories"].remove(directory)
        self.config["recent_directories"].insert(0, directory)
        self.config["recent_directories"] = self.config["recent_directories"][:10]
    
    def clear_recent_directories(self) -> None:
        """Clear recent directories list"""
        self.config["recent_directories"] = []
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a configuration setting"""
        return self.config.get(key, default)
    
    def set_setting(self, key: str, value: Any) -> None:
        """Set a configuration setting"""
        self.config[key] = value
    
    def load_config(self) -> None:
        """Load configuration from file"""
        print(f"=== load_config called ===")
        print(f"Config file path: {self.config_file}")
        print(f"Config file exists: {os.path.exists(self.config_file)}")
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    print(f"Raw saved config: {saved_config}")
                    
                    # Update config
                    self.config.update(saved_config)
                    print(f"Config updated with saved content")
                    print(f"Config file loaded: {self.config_file}")
                    print(f"Loaded config content: {self.config}")
                    print(f"Loaded file_types: {list(self.config.get('file_types', {}).keys())}")
            except Exception as e:
                print(f"Config file loading error: {e}")
                import traceback
                traceback.print_exc()
                # Reset to defaults if loading fails
                self.config = self._get_default_config()
        else:
            print(f"Config file not found: {self.config_file}")
        
        # Set current language from config
        self.current_language = self.config.get("language", "ja")
        print(f"Current language set to: {self.current_language}")
        
        # Initialize file types if not present
        self._initialize_file_types()
    
    def _initialize_file_types(self) -> None:
        """Initialize file types from current language defaults if not present"""
        if not self.config.get("file_types"):
            print("No file types in config, initializing from current language defaults")
            if self.current_language in self.file_type_categories:
                self.config["file_types"] = self.file_type_categories[self.current_language].copy()
                print(f"Initialized file types for language '{self.current_language}': {list(self.config['file_types'].keys())}")
                self.save_config()
            else:
                print(f"Language '{self.current_language}' not found in file type categories")
        else:
            print(f"File types already present in config: {list(self.config['file_types'].keys())}")
            
            # Check if we need to merge with current language defaults
            current_file_types = self.config.get("file_types", {})
            if self.current_language in self.file_type_categories:
                current_defaults = self.file_type_categories[self.current_language]
                
                # Get deleted default categories for current language
                deleted_defaults = self.config.get("deleted_default_categories", [])
                deleted_categories = set()
                
                for deletion_info in deleted_defaults:
                    if isinstance(deletion_info, dict):
                        deleted_category = deletion_info.get("category")
                        deleted_language = deletion_info.get("language")
                        deleted_extensions = deletion_info.get("extensions")
                        
                        # Check if this deletion applies to current language
                        if deleted_language == self.current_language:
                            deleted_categories.add(deleted_category)
                            print(f"  '{deleted_category}' is marked as deleted for current language")
                        else:
                            # Check if extensions match any category in current language
                            for current_category, current_extensions in current_defaults.items():
                                if current_extensions == deleted_extensions:
                                    deleted_categories.add(current_category)
                                    print(f"  '{current_category}' is marked as deleted (equivalent to '{deleted_category}' from '{deleted_language}')")
                                    break
                    elif isinstance(deletion_info, str):
                        # Handle old string format
                        if deletion_info in current_defaults:
                            deleted_categories.add(deletion_info)
                            print(f"  '{deletion_info}' is marked as deleted (old format)")
                
                print(f"Deleted categories for current language: {list(deleted_categories)}")
                
                # Check if any current language defaults are missing (excluding deleted ones)
                missing_defaults = {}
                for category, extensions in current_defaults.items():
                    if category not in current_file_types and category not in deleted_categories:
                        missing_defaults[category] = extensions
                
                if missing_defaults:
                    print(f"Adding missing default categories for language '{self.current_language}': {list(missing_defaults.keys())}")
                    
                    # Add missing defaults
                    for category, extensions in missing_defaults.items():
                        current_file_types[category] = extensions
                    
                    # Update config
                    self.config["file_types"] = current_file_types
                    self.save_config()
                    print(f"Updated file types: {list(current_file_types.keys())}")
                else:
                    print(f"No missing default categories to add (all defaults present or deleted)")
    
    def save_config(self) -> None:
        """Save configuration to file"""
        try:
            print(f"=== save_config called ===")
            print(f"Config file path: {self.config_file}")
            print(f"Current config state:")
            print(f"  - file_types count: {len(self.config.get('file_types', {}))}")
            print(f"  - file_types keys: {list(self.config.get('file_types', {}).keys())}")
            print(f"  - language: {self.config.get('language', 'unknown')}")
            
            # Ensure directory exists
            config_dir = os.path.dirname(self.config_file)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir, exist_ok=True)
                print(f"Directory created: {config_dir}")
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            
            print(f"Config file saved: {self.config_file}")
            print(f"Saved categories count: {len(self.config.get('file_types', {}))}")
            
            # Verify file was created
            if os.path.exists(self.config_file):
                print(f"✓ File created successfully: {self.config_file}")
                
                # Verify the saved content
                try:
                    with open(self.config_file, 'r', encoding='utf-8') as f:
                        saved_content = json.load(f)
                    print(f"✓ File content verified:")
                    print(f"  - Saved file_types count: {len(saved_content.get('file_types', {}))}")
                    print(f"  - Saved file_types keys: {list(saved_content.get('file_types', {}).keys())}")
                except Exception as verify_error:
                    print(f"✗ Error verifying saved content: {verify_error}")
            else:
                print(f"✗ File was not created: {self.config_file}")
                
        except Exception as e:
            print(f"Config save error: {e}")
            import traceback
            traceback.print_exc()
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults"""
        self.config = self._get_default_config()
        self.current_language = "ja"
        self.save_config()

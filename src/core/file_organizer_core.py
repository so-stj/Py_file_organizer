#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Organizer Core
Responsible for file organization business logic, file categorization, and file operations
"""

import os
import shutil
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set


class FileOrganizerCore:
    """Core file organization logic"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
    
    def categorize_file(self, file_path: Path) -> str:
        """Categorize a file based on its extension"""
        file_extension = file_path.suffix.lower()
        
        # Check if extension matches any category
        file_types = self.config_manager.get_file_types()
        for category, extensions in file_types.items():
            if file_extension in extensions:
                return category
        
        # Return "other" if no category matches
        return self.config_manager.get_text("other")
    
    def organize_single_file(self, file_path: Path, target_path: Path) -> Tuple[bool, str]:
        """Organize a single file to its appropriate category folder"""
        try:
            # Determine file category
            category = self.categorize_file(file_path)
            
            # Create category directory
            category_path = target_path / category
            category_path.mkdir(exist_ok=True)
            
            # Create date folder if enabled
            if self.config_manager.get_setting("create_date_folders", True):
                file_date = datetime.fromtimestamp(file_path.stat().st_mtime)
                date_folder = file_date.strftime("%Y-%m")
                category_path = category_path / date_folder
                category_path.mkdir(exist_ok=True)
            
            # Determine destination path
            destination = category_path / file_path.name
            
            # Handle duplicate files if enabled
            if destination.exists() and self.config_manager.get_setting("move_duplicates", True):
                destination = self._generate_unique_filename(destination)
            
            # Move file
            shutil.move(str(file_path), str(destination))
            
            # Log the operation
            log_message = f"{self.config_manager.get_text('move_file')} {file_path.name} → {category}/{destination.name}"
            
            return True, log_message
            
        except Exception as e:
            error_message = f"Error organizing {file_path.name}: {e}"
            return False, error_message
    
    def _generate_unique_filename(self, file_path: Path) -> Path:
        """Generate a unique filename to avoid conflicts"""
        base_name = file_path.stem
        extension = file_path.suffix
        counter = 1
        
        while file_path.exists():
            new_name = f"{base_name}_{counter}{extension}"
            file_path = file_path.parent / new_name
            counter += 1
        
        return file_path
    
    def search_files(self, source_path: Path, pattern: str) -> List[Path]:
        """Search for files matching a pattern"""
        matching_files = []
        
        try:
            for file_path in source_path.rglob("*"):
                if file_path.is_file():
                    if re.search(pattern, file_path.name, re.IGNORECASE):
                        matching_files.append(file_path)
        except Exception as e:
            print(f"Search error: {e}")
        
        return matching_files
    
    def separate_files(self, source_path: Path, target_path: Path, pattern: str, 
                      custom_folder_name: Optional[str] = None) -> Tuple[int, Path]:
        """Separate files matching a pattern to a separate directory"""
        try:
            # Create separation directory with custom name or timestamp
            if custom_folder_name:
                separate_path = target_path / custom_folder_name
            else:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                separate_path = target_path / f"分離_{timestamp}"
            
            separate_path.mkdir(parents=True, exist_ok=True)
            
            # Find matching files
            matching_files = self.search_files(source_path, pattern)
            
            moved_count = 0
            for file_path in matching_files:
                try:
                    destination = separate_path / file_path.name
                    
                    # Handle duplicates
                    if destination.exists():
                        destination = self._generate_unique_filename(destination)
                    
                    # Move file
                    shutil.move(str(file_path), str(destination))
                    moved_count += 1
                    
                except Exception as e:
                    print(f"Error moving {file_path.name}: {e}")
            
            return moved_count, separate_path
            
        except Exception as e:
            print(f"Separation error: {e}")
            return 0, target_path
    
    def move_files_to_existing_folder(self, source_path: Path, target_folder: Path, pattern: str) -> Tuple[int, Path]:
        """Move files matching a pattern directly to an existing folder (no subfolder creation)"""
        try:
            # Find matching files
            matching_files = self.search_files(source_path, pattern)
            
            moved_count = 0
            for file_path in matching_files:
                try:
                    destination = target_folder / file_path.name
                    
                    # Handle duplicates
                    if destination.exists():
                        destination = self._generate_unique_filename(destination)
                    
                    # Move file
                    shutil.move(str(file_path), str(destination))
                    moved_count += 1
                    
                except Exception as e:
                    print(f"Error moving {file_path.name}: {e}")
            
            return moved_count, target_folder
            
        except Exception as e:
            print(f"Move to existing folder error: {e}")
            return 0, target_folder
    
    def get_files_for_organization(self, source_path: Path) -> List[Path]:
        """Get list of files to organize from source directory"""
        try:
            if not source_path.exists():
                return []
            
            files = [f for f in source_path.iterdir() if f.is_file()]
            return files
        except Exception as e:
            print(f"Error getting files: {e}")
            return []
    
    def validate_directories(self, source_path: str, target_path: str) -> Tuple[bool, str]:
        """Validate source and target directories"""
        if not source_path or not target_path:
            return False, self.config_manager.get_text("error_source_target_required")
        
        source = Path(source_path)
        if not source.exists():
            return False, f"{self.config_manager.get_text('error_source_not_exists')} {source_path}"
        
        return True, ""
    
    def validate_search_pattern(self, pattern: str) -> Tuple[bool, str]:
        """Validate search pattern"""
        if not pattern:
            return False, self.config_manager.get_text("error_pattern_required")
        return True, ""

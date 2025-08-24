#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テスト用サンプルファイル作成スクリプト
ファイル仕分けシステムのテスト用に様々な種類のファイルを作成します
"""

import os
import random
from pathlib import Path
from datetime import datetime, timedelta

def create_test_files():
    """テスト用ファイルを作成"""
    
    # テストディレクトリを作成
    test_dir = Path("test_files")
    test_dir.mkdir(exist_ok=True)
    
    # ファイルタイプとサンプル内容
    file_types = {
        "画像": {
            "extensions": [".jpg", ".png", ".gif"],
            "content": "This is a sample image file.\n"
        },
        "動画": {
            "extensions": [".mp4", ".avi", ".mov"],
            "content": "This is a sample video file.\n"
        },
        "音声": {
            "extensions": [".mp3", ".wav", ".flac"],
            "content": "This is a sample audio file.\n"
        },
        "文書": {
            "extensions": [".pdf", ".txt", ".doc"],
            "content": "This is a sample document file.\n"
        },
        "スプレッドシート": {
            "extensions": [".xlsx", ".csv"],
            "content": "This is a sample spreadsheet file.\n"
        },
        "プレゼンテーション": {
            "extensions": [".pptx", ".ppt"],
            "content": "This is a sample presentation file.\n"
        },
        "アーカイブ": {
            "extensions": [".zip", ".rar"],
            "content": "This is a sample archive file.\n"
        },
        "実行ファイル": {
            "extensions": [".exe", ".msi"],
            "content": "This is a sample executable file.\n"
        },
        "コード": {
            "extensions": [".py", ".js", ".html", ".css"],
            "content": "This is a sample code file.\n"
        }
    }
    
    # ファイル名のプレフィックス
    prefixes = [
        "report", "document", "image", "video", "audio", "backup", 
        "test", "sample", "work", "project", "meeting", "presentation"
    ]
    
    created_files = []
    
    print("テストファイルを作成中...")
    
    # 各カテゴリでファイルを作成
    for category, info in file_types.items():
        for ext in info["extensions"]:
            # 複数のファイルを作成
            for i in range(random.randint(2, 5)):
                prefix = random.choice(prefixes)
                filename = f"{prefix}_{category.lower()}_{i+1}{ext}"
                file_path = test_dir / filename
                
                # ファイルを作成
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Category: {category}\n")
                    f.write(f"Extension: {ext}\n")
                    f.write(f"Created: {datetime.now()}\n")
                    f.write(info["content"])
                
                # ファイルのタイムスタンプをランダムに設定（過去30日以内）
                days_ago = random.randint(0, 30)
                timestamp = datetime.now() - timedelta(days=days_ago)
                os.utime(file_path, (timestamp.timestamp(), timestamp.timestamp()))
                
                created_files.append(filename)
    
    # 特殊な名前のファイルも作成
    special_files = [
        "2023_report.pdf",
        "2024_budget.xlsx", 
        "backup_20231201.zip",
        "meeting_notes_2024.txt",
        "project_document_v2.docx"
    ]
    
    for filename in special_files:
        file_path = test_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"Special file: {filename}\n")
            f.write(f"Created: {datetime.now()}\n")
        
        # ランダムなタイムスタンプ
        days_ago = random.randint(0, 30)
        timestamp = datetime.now() - timedelta(days=days_ago)
        os.utime(file_path, (timestamp.timestamp(), timestamp.timestamp()))
        
        created_files.append(filename)
    
    print(f"✅ {len(created_files)}個のテストファイルを作成しました。")
    print(f"📁 保存場所: {test_dir.absolute()}")
    print("\n作成されたファイル:")
    for filename in sorted(created_files):
        print(f"  - {filename}")
    
    print(f"\n🎯 ファイル仕分けシステムを起動して、'{test_dir}' をソースディレクトリとして選択してください。")

if __name__ == "__main__":
    create_test_files()

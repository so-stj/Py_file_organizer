#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Entry Point
Entry point for the refactored File Organizer application
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main_app import FileOrganizerApp


def main():
    """Main entry point"""
    try:
        app = FileOrganizerApp()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

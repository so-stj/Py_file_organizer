# File Organizer GUI Application ![Logo](icon.ico)

An automated file classification and GUI-operated file management application with multilingual support.

## Features

### 🗂️ Automatic File Organization
- Automatically classify files by category based on file extensions
- Auto-recognition of images, videos, audio, documents, spreadsheets, presentations, archives, executables, and code files
- Optional date-based folder creation
- Automatic renaming of duplicate files

### 🔍 File Search & Separation
- Advanced file search using regular expressions
- Display of search results
- Bulk separation of matching files

### 🌍 Multilingual Support
- Support for Japanese, English, and Swedish
- Language selection dialog on first startup
- Dynamic language switching in settings
- Localized UI elements and messages

### ⚙️ Customizable Settings
- Add, edit, and delete file types
- Customize organization rules
- Persistent settings with configuration file
- Language preferences

### 🛠️ Maintenance Features
- Clear cache (recent directories)
- Reset all settings to defaults
- Reset language selection for first startup dialog
- Configuration file management

### 📊 Real-time Monitoring
- Progress bar showing processing status
- Detailed operation logs
- Stop/resume processing functionality

## Installation

### Requirements
- Python 3.6 or higher
- tkinter (usually included with Python)

### How to Run
```bash
python file_organizer.py
```

## Usage

### 1. First Startup
- Language selection dialog appears on first run
- Choose your preferred language (Japanese, English, or Swedish)
- You can change the language later in Settings

### 2. Basic File Organization

1. **Select Source Directory**
   - Click "Browse" to select the folder containing files to organize

2. **Select Target Directory**
   - Click "Browse" to select the folder where organized files will be saved

3. **Start Automatic Organization**
   - Click "Start Auto Organization" button
   - Monitor progress with the progress bar
   - Check detailed processing in the log area

### 3. File Search & Separation

1. **Enter Search Pattern**
   - Enter a regular expression search pattern
   - Examples: `\.jpg$` (JPG files), `report.*\.pdf` (PDF files starting with "report")

2. **Execute Search**
   - Click "Search" to find matching files
   - Search results are displayed in the result area

3. **Separate Files**
   - Click "Separate Matching Files" to move them
   - Matching files are moved to a timestamped dedicated folder

### 4. Customize Settings

1. **Open Settings Window**
   - Click "Settings" button

2. **File Types Tab**
   - Add, edit, delete categories and extensions
   - Create custom organization rules
   - Categories are preserved across language changes

3. **Language Tab**
   - Change application language
   - Japanese, English, and Swedish support
   - Restart required after language change

4. **Maintenance Tab**
   - **Clear Cache**: Remove recent directories from history
   - **Reset to Defaults**: Reset all settings to initial state
   - **Reset Language Selection**: Show language dialog on next startup

5. **General Settings**
   - Enable/disable auto organization
   - Enable/disable date folder creation
   - Duplicate file handling settings

## File Type Configuration

### Default Categories

| Category | Extensions |
|---------|--------|
| Images | .jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp |
| Videos | .mp4, .avi, .mov, .wmv, .flv, .mkv, .webm |
| Audio | .mp3, .wav, .flac, .aac, .ogg, .wma |
| Documents | .pdf, .doc, .docx, .txt, .rtf, .odt |
| Spreadsheets | .xls, .xlsx, .csv, .ods |
| Presentations | .ppt, .pptx, .odp |
| Archives | .zip, .rar, .7z, .tar, .gz |
| Executables | .exe, .msi, .dmg, .deb, .rpm |
| Code | .py, .js, .html, .css, .java, .cpp, .c, .php |

### Adding Custom Categories

1. Open Settings window
2. Select "File Types" tab
3. Click "Add" button
4. Enter category name and extensions
5. Click "OK"

**Note**: Custom categories are preserved when changing languages and persist across application restarts.

## Configuration File

The application saves settings to a configuration file:

- **Windows**: `%LOCALAPPDATA%\FileOrganizer\file_organizer_config.json`
- **Linux/Mac**: `./file_organizer_config.json` (in application directory)

### Configuration Contents
```json
{
  "file_types": { /* Custom file type categories */ },
  "recent_directories": [ /* Recently used directories */ ],
  "auto_organize": true,
  "create_date_folders": true,
  "move_duplicates": true,
  "language": "ja",
  "language_selected": true
}
```

## Search Pattern Examples

| Pattern | Description |
|---------|------|
| `\.jpg$` | JPG files only |
| `report.*\.pdf` | PDF files starting with "report" |
| `202[0-9]` | Files from 2020s |
| `\.(jpg\|png\|gif)$` | Image files (JPG, PNG, GIF) |
| `backup.*` | Files starting with "backup" |

## Important Notes

⚠️ **Important Warnings**

- File move operations cannot be undone
- Please backup important files before processing
- Ensure sufficient disk space when processing large numbers of files
- Do not move or delete files during processing
- Custom categories are preserved across language changes

## Troubleshooting

### Common Issues

**Q: Files are not moving**
A: Check if files are not being used by other applications

**Q: Permission errors occur**
A: Run with administrator privileges or check directory access permissions

**Q: Settings are not saved**
A: Check write permissions for the configuration file

**Q: Language doesn't change**
A: Restart the application after changing the language

**Q: Custom categories disappear**
A: Custom categories are preserved across language changes. Check the File Types tab in Settings.

## License

This project is released under the MIT License.

## Version History

- v1.1.0: Multilingual Support & Maintenance Features
  - Added Japanese, English, and Swedish language support
  - Language selection dialog on first startup
  - Maintenance features (cache clear, reset defaults, reset language)
  - Enhanced configuration file management
  - Custom categories preservation across language changes

- v1.0.0: Initial Release
  - Basic file organization functionality
  - GUI operation interface
  - File search and separation functionality
  - Settings customization functionality

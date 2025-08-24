# File Organizer System

An automated file classification and GUI-operated file management application.

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

### ⚙️ Customizable Settings
- Add, edit, and delete file types
- Customize organization rules
- Persistent settings

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

### 1. Basic File Organization

1. **Select Source Directory**
   - Click "Browse" to select the folder containing files to organize

2. **Select Target Directory**
   - Click "Browse" to select the folder where organized files will be saved

3. **Start Automatic Organization**
   - Click "Start Auto Organization" button
   - Monitor progress with the progress bar
   - Check detailed processing in the log area

### 2. File Search & Separation

1. **Enter Search Pattern**
   - Enter a regular expression search pattern
   - Examples: `\.jpg$` (JPG files), `report.*\.pdf` (PDF files starting with "report")

2. **Execute Search**
   - Click "Search" to find matching files
   - Search results are displayed in the result area

3. **Separate Files**
   - Click "Separate Matching Files" to move them
   - Matching files are moved to a timestamped dedicated folder

### 3. Customize Settings

1. **Open Settings Window**
   - Click "Settings" button

2. **Manage File Types**
   - Use "File Types" tab to add, edit, delete categories and extensions
   - Add new categories to create custom organization rules

3. **General Settings**
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

## Troubleshooting

### Common Issues

**Q: Files are not moving**
A: Check if files are not being used by other applications

**Q: Permission errors occur**
A: Run with administrator privileges or check directory access permissions

**Q: Settings are not saved**
A: Check write permissions for the configuration file

## License

This project is released under the MIT License.

## Version History

- v1.0.0: Initial Release
  - Basic file organization functionality
  - GUI operation interface
  - File search and separation functionality
  - Settings customization functionality

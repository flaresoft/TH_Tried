# TH_Tried

This repository contains a sample Python application `audio_browser.py`.
The tool scans all mounted drives for audio files, caches their paths in a
SQLite database, and provides a GUI to browse and preview them. Use the menu
option to configure preview duration. Selected files can be dragged to external
applications that accept drag-and-drop, such as a DAW.

## Building an executable

1. Install PyInstaller:
   
   ```bash
   pip install pyinstaller
   ```

2. Run the build script to create a standalone executable:
   
   ```bash
   python build_exe.py
   ```

The generated binary will be located in the `dist` directory.

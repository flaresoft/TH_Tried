# TH Tried

This repository contains a small example application `sound_browser.py`.

The program provides a desktop interface for exploring audio files on your PC.
Key features:

* Scan a directory for audio files (`.wav`, `.mp3`, `.flac`, `.ogg`, `.aiff`).
* Search and filter files through a text box.
* Display basic metadata and a waveform preview of the selected file.
* Play or stop the file immediately.
* Drag & drop files directly to other applications (e.g. a DAW).
* Cache metadata to a JSON file so subsequent runs are faster.

## Usage

Install requirements and run the application:

```bash
pip install PyQt5 pyqtgraph numpy
python sound_browser.py
```

When launched, choose **File → Scan directory** to select a folder to scan.

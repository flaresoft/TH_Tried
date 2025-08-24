# TH_Tried

Utility for measuring the integrated loudness (LUFS) of audio files.

## lufs_meter.py

`lufs_meter.py` uses `ffmpeg`'s `ebur128` filter to calculate LUFS for
common audio formats such as MP3 and WAV. It supports scanning
directories as well as an optional drag & drop GUI.

### Requirements
- Python 3.12+
- `ffmpeg` installed and available on `PATH`
- Optional: `tkinterdnd2` for drag & drop GUI support

### Command line usage
```bash
python lufs_meter.py song.mp3 another.wav
python lufs_meter.py --scan path/to/folder
```

### GUI usage
```bash
python lufs_meter.py --gui
```
Drag audio files into the window (requires `tkinterdnd2`) or drop files
onto the script icon on supported platforms.

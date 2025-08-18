#!/usr/bin/env python3
"""
Sound file browser with simple caching and drag-and-drop support.

This GUI application lets you scan directories for sound files, preview them
immediately and drag them into other applications such as a DAW. Previously
scanned files are cached on disk so later launches load the metadata faster.

Requirements: PyQt5, pyqtgraph
"""
import json
import os
import sys
import wave
from pathlib import Path

from PyQt5.QtCore import Qt, QMimeData, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

import numpy as np
import pyqtgraph as pg

AUDIO_EXT = {".wav", ".mp3", ".flac", ".ogg", ".aiff"}
CACHE_FILE = Path.home() / "sound_cache.json"


class Cache:
    """Simple JSON based cache for metadata."""

    def __init__(self) -> None:
        self.data = {}
        if CACHE_FILE.exists():
            try:
                self.data = json.loads(CACHE_FILE.read_text())
            except Exception:
                self.data = {}

    def save(self) -> None:
        CACHE_FILE.write_text(json.dumps(self.data))

    def get(self, path: str, mtime: float):
        info = self.data.get(path)
        if info and info.get("mtime") == mtime:
            return info
        return None

    def set(self, path: str, mtime: float, info: dict) -> None:
        info["mtime"] = mtime
        self.data[path] = info


class SoundBrowser(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Sound Browser")
        self.cache = Cache()
        self.player = QMediaPlayer(self)
        self._build_ui()

    def _build_ui(self) -> None:
        main = QWidget()
        self.setCentralWidget(main)
        layout = QHBoxLayout(main)
        splitter = QSplitter()
        layout.addWidget(splitter)

        # Left panel: search + file list
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search")
        self.search_bar.textChanged.connect(self._update_filter)
        left_layout.addWidget(self.search_bar)

        self.file_list = QListWidget()
        self.file_list.setDragEnabled(True)
        self.file_list.itemSelectionChanged.connect(self._display_selected)
        left_layout.addWidget(self.file_list)
        splitter.addWidget(left_widget)

        # Right panel: metadata + waveform + controls
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        self.meta_label = QLabel("Select a file to see metadata")
        right_layout.addWidget(self.meta_label)

        self.wave_plot = pg.PlotWidget()
        self.wave_plot.setYRange(-1, 1)
        self.cursor_line = self.wave_plot.addLine(x=0, pen="r")
        right_layout.addWidget(self.wave_plot)

        controls = QHBoxLayout()
        self.play_btn = QPushButton("Play")
        self.play_btn.clicked.connect(self._play)
        controls.addWidget(self.play_btn)
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.player.stop)
        controls.addWidget(self.stop_btn)
        right_layout.addLayout(controls)

        splitter.addWidget(right_widget)
        splitter.setSizes([250, 500])

        # Menu
        file_menu = self.menuBar().addMenu("File")
        open_act = file_menu.addAction("Scan directory")
        open_act.triggered.connect(self._scan_directory)

    def _scan_directory(self) -> None:
        path = QFileDialog.getExistingDirectory(
            self, "Select directory", str(Path.home())
        )
        if not path:
            return
        path = Path(path)
        self.file_list.clear()
        for root, _, files in os.walk(path):
            for name in files:
                if Path(name).suffix.lower() in AUDIO_EXT:
                    full = str(Path(root) / name)
                    item = QListWidgetItem(full)
                    self.file_list.addItem(item)
        self._update_filter()

    def _update_filter(self) -> None:
        text = self.search_bar.text().lower()
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            item.setHidden(text not in item.text().lower())

    def _display_selected(self) -> None:
        items = self.file_list.selectedItems()
        if not items:
            return
        path = items[0].text()
        p = Path(path)
        mtime = p.stat().st_mtime
        meta = self.cache.get(path, mtime)
        if not meta:
            meta = self._read_metadata(p)
            self.cache.set(path, mtime, meta)
            self.cache.save()
        self.meta_label.setText("\n".join(f"{k}: {v}" for k, v in meta.items()))
        self._load_waveform(p)

    def _read_metadata(self, path: Path) -> dict:
        info = {"path": str(path)}
        try:
            with wave.open(str(path), "rb") as w:
                info.update(
                    {
                        "channels": w.getnchannels(),
                        "sample_width": w.getsampwidth(),
                        "frame_rate": w.getframerate(),
                        "frames": w.getnframes(),
                        "duration": w.getnframes() / w.getframerate(),
                    }
                )
        except wave.Error:
            pass
        return info

    def _load_waveform(self, path: Path) -> None:
        try:
            with wave.open(str(path), "rb") as w:
                frames = w.readframes(w.getnframes())
                dtype = np.int16 if w.getsampwidth() == 2 else np.int8
                arr = np.frombuffer(frames, dtype=dtype)
                if w.getnchannels() > 1:
                    arr = arr[:: w.getnchannels()]
                arr = arr / np.max(np.abs(arr))
                self.wave_plot.plot(arr, clear=True)
                self.cursor_line.setValue(0)
                self.player.setMedia(QMediaContent(QUrl.fromLocalFile(str(path))))
        except Exception:
            self.wave_plot.plot([], clear=True)

    def _play(self) -> None:
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_btn.setText("Play")
        else:
            self.player.play()
            self.play_btn.setText("Pause")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SoundBrowser()
    win.resize(800, 600)
    win.show()
    sys.exit(app.exec_())

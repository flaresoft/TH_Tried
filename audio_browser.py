import os
import sys
import sqlite3
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia
import psutil

AUDIO_EXTENSIONS = {'.wav', '.mp3', '.flac', '.ogg', '.aiff', '.aif', '.m4a'}
DB_FILE = 'audio_cache.db'
PREVIEW_SECONDS_DEFAULT = 5

class AudioBrowser(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.preview_seconds = PREVIEW_SECONDS_DEFAULT
        self.db = sqlite3.connect(DB_FILE)
        self.ensure_db()
        self.init_ui()
        self.media_player = QtMultimedia.QMediaPlayer()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.stop_preview)
        self.scan_drives()

    def ensure_db(self):
        cur = self.db.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS audio_files (
            path TEXT PRIMARY KEY,
            mtime REAL
            )"""
        )
        self.db.commit()

    def init_ui(self):
        self.setWindowTitle("Audio Browser")
        self.resize(800, 600)
        self.model = QtWidgets.QFileSystemModel()
        self.model.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot)
        self.model.setNameFilters(["*" + ext for ext in AUDIO_EXTENSIONS])
        self.model.setNameFilterDisables(False)

        self.tree = QtWidgets.QTreeView()
        self.tree.setModel(self.model)
        self.tree.setDragEnabled(True)
        self.setCentralWidget(self.tree)
        self.tree.doubleClicked.connect(self.on_double_click)
        self.tree.installEventFilter(self)

        menubar = self.menuBar()
        options_menu = menubar.addMenu("Options")
        duration_action = QtWidgets.QAction("Set Preview Duration", self)
        duration_action.triggered.connect(self.set_preview_duration)
        options_menu.addAction(duration_action)

    def scan_drives(self):
        cur = self.db.cursor()
        existing = {row[0]: row[1] for row in cur.execute("SELECT path, mtime FROM audio_files")}
        found = {}
        for part in psutil.disk_partitions():
            root = part.mountpoint
            for base, dirs, files in os.walk(root):
                for name in files:
                    if os.path.splitext(name)[1].lower() in AUDIO_EXTENSIONS:
                        path = os.path.join(base, name)
                        try:
                            mtime = os.path.getmtime(path)
                        except OSError:
                            continue
                        found[path] = mtime
        # update db
        to_add = [(p, m) for p, m in found.items() if p not in existing or existing[p] != m]
        to_remove = [p for p in existing if p not in found]
        if to_add:
            cur.executemany("REPLACE INTO audio_files(path, mtime) VALUES (?, ?)", to_add)
        if to_remove:
            cur.executemany("DELETE FROM audio_files WHERE path=?", [(p,) for p in to_remove])
        self.db.commit()

    def eventFilter(self, source, event):
        if source is self.tree and event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Space:
                index = self.tree.currentIndex()
                path = self.model.filePath(index)
                if os.path.isfile(path):
                    self.preview(path)
                return True
        return super().eventFilter(source, event)

    def on_double_click(self, index):
        path = self.model.filePath(index)
        if os.path.isfile(path) and os.path.splitext(path)[1].lower() in AUDIO_EXTENSIONS:
            self.preview(path)

    def preview(self, path):
        url = QtCore.QUrl.fromLocalFile(path)
        content = QtMultimedia.QMediaContent(url)
        self.media_player.setMedia(content)
        self.media_player.play()
        self.timer.start(self.preview_seconds * 1000)

    def stop_preview(self):
        self.media_player.stop()
        self.timer.stop()

    def set_preview_duration(self):
        seconds, ok = QtWidgets.QInputDialog.getInt(
            self, "Preview Duration", "Seconds:", value=self.preview_seconds, min=1, max=60
        )
        if ok:
            self.preview_seconds = seconds

    def closeEvent(self, event):
        self.db.close()
        return super().closeEvent(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    browser = AudioBrowser()
    browser.show()
    sys.exit(app.exec_())

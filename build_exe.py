import PyInstaller.__main__


def build():
    PyInstaller.__main__.run([
        "audio_browser.py",
        "--onefile",
        "--windowed",
        "--name", "audio_browser",
    ])


if __name__ == "__main__":
    build()

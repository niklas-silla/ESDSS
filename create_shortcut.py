"""
create_shortcut.py — Run this ONCE to create the ESDSS desktop shortcut.
Works on macOS, Windows, and Linux.
"""

import os
import sys
import stat
import platform
import textwrap
from pathlib import Path

REPO_DIR = Path(__file__).parent.resolve()
START_SCRIPT = REPO_DIR / "start.py"
DESKTOP = Path.home() / "Desktop"

# Find the Python executable that is running this script
PYTHON = sys.executable


def create_macos():
    app = DESKTOP / "ESDSS.app"
    macos_dir = app / "Contents" / "MacOS"
    macos_dir.mkdir(parents=True, exist_ok=True)

    # Info.plist
    (app / "Contents" / "Info.plist").write_text(textwrap.dedent(f"""\
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
            "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict>
            <key>CFBundleExecutable</key>
            <string>ESDSS</string>
            <key>CFBundleName</key>
            <string>ESDSS</string>
            <key>CFBundleDisplayName</key>
            <string>ESDSS</string>
            <key>CFBundleVersion</key>
            <string>1.0</string>
            <key>CFBundlePackageType</key>
            <string>APPL</string>
        </dict>
        </plist>
    """))

    # Launcher executable inside the .app
    launcher = macos_dir / "ESDSS"
    launcher.write_text(f'#!/bin/bash\n"{PYTHON}" "{START_SCRIPT}"\n')
    launcher.chmod(launcher.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

    # Remove quarantine flag so macOS doesn't block it
    os.system(f'xattr -cr "{app}" 2>/dev/null')

    print(f"Shortcut created: {app}")
    print("Double-click ESDSS on your Desktop to launch the application.")


def create_windows():
    shortcut = DESKTOP / "ESDSS.vbs"
    # VBScript launches start.py without showing a console window
    shortcut.write_text(textwrap.dedent(f"""\
        Set WshShell = CreateObject("WScript.Shell")
        WshShell.Run Chr(34) & "{PYTHON}" & Chr(34) & " " & Chr(34) & "{START_SCRIPT}" & Chr(34), 0, False
    """))
    print(f"Shortcut created: {shortcut}")
    print("Double-click ESDSS on your Desktop to launch the application.")


def create_linux():
    shortcut = DESKTOP / "ESDSS.desktop"
    shortcut.write_text(textwrap.dedent(f"""\
        [Desktop Entry]
        Version=1.0
        Type=Application
        Name=ESDSS
        Comment=Editorial Screening Decision Support System
        Exec={PYTHON} {START_SCRIPT}
        Terminal=false
        Categories=Science;
    """))
    shortcut.chmod(shortcut.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    print(f"Shortcut created: {shortcut}")
    print("Double-click ESDSS on your Desktop to launch the application.")


def main():
    if not DESKTOP.exists():
        print(f"Desktop folder not found at: {DESKTOP}")
        print("Please move the created shortcut file manually.")
        DESKTOP.mkdir(exist_ok=True)

    system = platform.system()
    if system == "Darwin":
        create_macos()
    elif system == "Windows":
        create_windows()
    elif system == "Linux":
        create_linux()
    else:
        print(f"Unsupported OS: {system}")
        sys.exit(1)


if __name__ == "__main__":
    main()

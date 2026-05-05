"""
create_shortcut.py — Run this ONCE to create the ESDSS desktop shortcut.
Works on macOS, Windows, and Linux.
"""

import os
import sys
import stat
import platform
import textwrap
import subprocess
from pathlib import Path

REPO_DIR = Path(__file__).parent.resolve()
START_SCRIPT = REPO_DIR / "start.py"
DESKTOP = Path.home() / "Desktop"
SYSTEM = platform.system()


def find_python_with_uvicorn() -> str:
    """Return the Python executable that can import uvicorn."""
    candidates = [sys.executable]

    conda_roots = [
        Path.home() / "anaconda3",
        Path.home() / "miniconda3",
        Path("/opt/homebrew/anaconda3"),
        Path("/opt/homebrew/miniconda3"),
        Path("/opt/anaconda3"),
        Path("/usr/local/anaconda3"),
        Path("/usr/local/miniconda3"),
    ]
    suffix = "Scripts/python.exe" if SYSTEM == "Windows" else "bin/python"
    for root in conda_roots:
        candidates.append(root / "envs" / "esdss" / suffix)

    for c in candidates:
        path = str(c)
        result = subprocess.run(
            [path, "-c", "import uvicorn"],
            capture_output=True
        )
        if result.returncode == 0:
            return path

    # Nothing found — return sys.executable and let start.py show the error
    return sys.executable


def create_macos():
    python = find_python_with_uvicorn()
    app = DESKTOP / "ESDSS.app"
    macos_dir = app / "Contents" / "MacOS"
    macos_dir.mkdir(parents=True, exist_ok=True)

    (app / "Contents" / "Info.plist").write_text(textwrap.dedent("""\
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
            <key>LSUIElement</key>
            <false/>
        </dict>
        </plist>
    """))

    # The launcher sources conda (for PATH) then calls start.py with the
    # correct Python. This is necessary because macOS .app bundles launch
    # with a stripped PATH that doesn't include conda or homebrew.
    conda_sources = "\n".join(
        f'[ -f "{root}/etc/profile.d/conda.sh" ] && source "{root}/etc/profile.d/conda.sh" && conda activate esdss 2>/dev/null && break'
        for root in [
            str(Path.home() / "anaconda3"),
            str(Path.home() / "miniconda3"),
            "/opt/homebrew/anaconda3",
            "/opt/homebrew/miniconda3",
            "/opt/anaconda3",
            "/usr/local/anaconda3",
        ]
    )

    launcher = macos_dir / "ESDSS"
    launcher.write_text(textwrap.dedent(f"""\
        #!/bin/bash
        # Source conda so uvicorn and all packages are on PATH
        for _conda_root in \\
            "$HOME/anaconda3" "$HOME/miniconda3" \\
            "/opt/homebrew/anaconda3" "/opt/homebrew/miniconda3" \\
            "/opt/anaconda3" "/usr/local/anaconda3"; do
            if [ -f "$_conda_root/etc/profile.d/conda.sh" ]; then
                source "$_conda_root/etc/profile.d/conda.sh"
                conda activate esdss 2>/dev/null
                break
            fi
        done

        # Also activate local venv as fallback
        [ -f "{REPO_DIR}/venv/bin/activate" ] && source "{REPO_DIR}/venv/bin/activate"

        "{python}" "{START_SCRIPT}"
    """))
    launcher.chmod(launcher.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

    # Remove quarantine so macOS doesn't block it on first run
    os.system(f'xattr -cr "{app}" 2>/dev/null')

    print(f"Shortcut created: {app}")
    print("Double-click ESDSS on your Desktop to launch the application.")


def create_windows():
    python = find_python_with_uvicorn()
    shortcut = DESKTOP / "ESDSS.vbs"
    shortcut.write_text(textwrap.dedent(f"""\
        Set WshShell = CreateObject("WScript.Shell")
        WshShell.Run Chr(34) & "{python}" & Chr(34) & " " & Chr(34) & "{START_SCRIPT}" & Chr(34), 0, False
    """))
    print(f"Shortcut created: {shortcut}")
    print("Double-click ESDSS on your Desktop to launch the application.")


def create_linux():
    python = find_python_with_uvicorn()
    shortcut = DESKTOP / "ESDSS.desktop"
    shortcut.write_text(textwrap.dedent(f"""\
        [Desktop Entry]
        Version=1.0
        Type=Application
        Name=ESDSS
        Comment=Editorial Screening Decision Support System
        Exec={python} {START_SCRIPT}
        Terminal=false
        Categories=Science;
    """))
    shortcut.chmod(shortcut.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    print(f"Shortcut created: {shortcut}")
    print("Double-click ESDSS on your Desktop to launch the application.")


def main():
    DESKTOP.mkdir(exist_ok=True)

    if SYSTEM == "Darwin":
        create_macos()
    elif SYSTEM == "Windows":
        create_windows()
    elif SYSTEM == "Linux":
        create_linux()
    else:
        print(f"Unsupported OS: {SYSTEM}")
        sys.exit(1)


if __name__ == "__main__":
    main()

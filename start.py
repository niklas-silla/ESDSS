"""
start.py — ESDSS Launcher
Run this file to start the ESDSS server and open the browser.
Works on macOS, Windows, and Linux.
"""

import os
import sys
import time
import signal
import platform
import subprocess
import urllib.request
from pathlib import Path

REPO_DIR = Path(__file__).parent.resolve()
PORT = 8000
URL = f"http://localhost:{PORT}"
PID_FILE = REPO_DIR / ".server.pid"
LOG_FILE = REPO_DIR / "logs" / "server.log"

SYSTEM = platform.system()


# ---------------------------------------------------------------------------
# Visible error dialog (so failures are never silent when launched as .app)
# ---------------------------------------------------------------------------

def show_error(msg: str):
    if SYSTEM == "Darwin":
        safe = msg.replace('"', "'")
        subprocess.run([
            "osascript", "-e",
            f'display dialog "{safe}" buttons {{"OK"}} default button "OK" with title "ESDSS – Error"'
        ])
    elif SYSTEM == "Windows":
        subprocess.run(
            ["powershell", "-Command",
             f'[System.Windows.Forms.MessageBox]::Show("{msg}", "ESDSS – Error")'],
            capture_output=True
        )
    else:
        print(f"ERROR: {msg}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Find uvicorn – checks every likely location before giving up
# ---------------------------------------------------------------------------

def find_uvicorn() -> str | None:
    candidates = []

    # 1. Same Python environment that is running this script right now
    python_dir = Path(sys.executable).parent
    candidates.append(python_dir / ("uvicorn.exe" if SYSTEM == "Windows" else "uvicorn"))

    # 2. Local venv inside the repo
    if SYSTEM == "Windows":
        candidates.append(REPO_DIR / "venv" / "Scripts" / "uvicorn.exe")
    else:
        candidates.append(REPO_DIR / "venv" / "bin" / "uvicorn")

    # 3. Common conda environment locations (env name = esdss)
    conda_roots = [
        Path.home() / "anaconda3",
        Path.home() / "miniconda3",
        Path("/opt/homebrew/anaconda3"),
        Path("/opt/homebrew/miniconda3"),
        Path("/opt/anaconda3"),
        Path("/usr/local/anaconda3"),
        Path("/usr/local/miniconda3"),
    ]
    for root in conda_roots:
        if SYSTEM == "Windows":
            candidates.append(root / "envs" / "esdss" / "Scripts" / "uvicorn.exe")
        else:
            candidates.append(root / "envs" / "esdss" / "bin" / "uvicorn")

    for c in candidates:
        if c.exists():
            return str(c)

    return None


# ---------------------------------------------------------------------------
# Server lifecycle
# ---------------------------------------------------------------------------

def server_is_running() -> bool:
    try:
        urllib.request.urlopen(URL, timeout=2)
        return True
    except Exception:
        return False


def kill_old_server():
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text().strip())
            os.kill(pid, signal.SIGTERM)
            time.sleep(1)
        except (ProcessLookupError, ValueError):
            pass
        PID_FILE.unlink(missing_ok=True)

    if SYSTEM in ("Darwin", "Linux"):
        subprocess.run(
            f"lsof -ti:{PORT} | xargs kill -9",
            shell=True, capture_output=True
        )
    elif SYSTEM == "Windows":
        result = subprocess.run(
            f"netstat -ano | findstr :{PORT}",
            shell=True, capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            parts = line.split()
            if parts:
                subprocess.run(f"taskkill /PID {parts[-1]} /F",
                               shell=True, capture_output=True)


def start_server(uvicorn: str):
    LOG_FILE.parent.mkdir(exist_ok=True)
    (REPO_DIR / "data" / "manuscripts").mkdir(parents=True, exist_ok=True)

    log = open(LOG_FILE, "a")

    flags = {}
    if SYSTEM == "Windows":
        flags["creationflags"] = subprocess.CREATE_NO_WINDOW

    proc = subprocess.Popen(
        [uvicorn, "server:app", "--port", str(PORT)],
        cwd=REPO_DIR,
        stdout=log,
        stderr=log,
        **flags,
    )
    PID_FILE.write_text(str(proc.pid))


def wait_for_server(timeout: int = 60) -> bool:
    for _ in range(timeout):
        if server_is_running():
            return True
        time.sleep(1)
    return False


def open_browser():
    if SYSTEM == "Darwin":
        subprocess.run(["open", URL])
    elif SYSTEM == "Windows":
        os.startfile(URL)
    else:
        subprocess.run(["xdg-open", URL])


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    try:
        # Already running → just open the browser
        if server_is_running():
            open_browser()
            return

        uvicorn = find_uvicorn()
        if uvicorn is None:
            show_error(
                "Could not find uvicorn.\n\n"
                "Make sure the 'esdss' conda environment is installed\n"
                "or that you have run: pip install -r requirements.txt"
            )
            sys.exit(1)

        kill_old_server()
        start_server(uvicorn)

        if not wait_for_server():
            show_error(
                "The server did not start within 60 seconds.\n\n"
                f"Check the log for details:\n{LOG_FILE}"
            )
            sys.exit(1)

        open_browser()

    except Exception as exc:
        show_error(f"Unexpected error:\n{exc}")
        raise


if __name__ == "__main__":
    main()

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

    # Also free port 8000 if something else holds it
    system = platform.system()
    if system in ("Darwin", "Linux"):
        subprocess.run(
            f"lsof -ti:{PORT} | xargs kill -9",
            shell=True, capture_output=True
        )
    elif system == "Windows":
        result = subprocess.run(
            f"netstat -ano | findstr :{PORT}",
            shell=True, capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            parts = line.split()
            if parts:
                pid = parts[-1]
                subprocess.run(f"taskkill /PID {pid} /F", shell=True, capture_output=True)


def find_uvicorn() -> str:
    """Return the uvicorn executable path, preferring the active venv."""
    system = platform.system()

    # Check local venv first
    if system == "Windows":
        venv_uvicorn = REPO_DIR / "venv" / "Scripts" / "uvicorn.exe"
    else:
        venv_uvicorn = REPO_DIR / "venv" / "bin" / "uvicorn"

    if venv_uvicorn.exists():
        return str(venv_uvicorn)

    # Fall back to whatever is on PATH
    return "uvicorn"


def start_server():
    LOG_FILE.parent.mkdir(exist_ok=True)
    (REPO_DIR / "data" / "manuscripts").mkdir(parents=True, exist_ok=True)

    uvicorn = find_uvicorn()
    log = open(LOG_FILE, "a")

    system = platform.system()
    if system == "Windows":
        # CREATE_NO_WINDOW prevents a console window from flashing
        proc = subprocess.Popen(
            [uvicorn, "server:app", "--port", str(PORT)],
            cwd=REPO_DIR,
            stdout=log,
            stderr=log,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
    else:
        proc = subprocess.Popen(
            [uvicorn, "server:app", "--port", str(PORT)],
            cwd=REPO_DIR,
            stdout=log,
            stderr=log,
        )

    PID_FILE.write_text(str(proc.pid))
    return proc


def wait_for_server(timeout: int = 60) -> bool:
    for _ in range(timeout):
        if server_is_running():
            return True
        time.sleep(1)
    return False


def open_browser():
    system = platform.system()
    if system == "Darwin":
        subprocess.run(["open", URL])
    elif system == "Windows":
        os.startfile(URL)
    else:
        subprocess.run(["xdg-open", URL])


def main():
    # If already running just open the browser
    if server_is_running():
        open_browser()
        return

    kill_old_server()
    start_server()

    ready = wait_for_server()
    if not ready:
        print(
            "Server did not start within 60 seconds.\n"
            f"Check the log for details: {LOG_FILE}"
        )
        sys.exit(1)

    open_browser()


if __name__ == "__main__":
    main()

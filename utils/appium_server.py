import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from appium.webdriver.appium_service import AppiumService


def is_appium_installed() -> bool:
    return shutil.which("appium") is not None


def get_appium_version() -> str | None:
    try:
        result = subprocess.run(
            ["appium", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


_service: AppiumService | None = None


def _wait_for_server(url: str, timeout: int = 30) -> None:
    health_url = f"{url.rstrip('/')}/status"
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            resp = urllib.request.urlopen(health_url, timeout=2)
            if resp.status == 200:
                return
        except (urllib.error.URLError, ConnectionError, TimeoutError):
            pass
        time.sleep(1)
    print(f"Appium server tidak merespon dalam {timeout} detik.", file=sys.stderr)
    sys.exit(1)


def start_appium_server(
    port: int = 4723,
    base_path: str = "/wd/hub",
    log_path: str | Path | None = None,
    wait_timeout: int = 30,
) -> AppiumService:
    global _service

    if not is_appium_installed():
        version = get_appium_version()
        if version:
            msg = (
                f"Appium terdeteksi tapi tidak bisa dijalankan (versi {version}). "
                "Periksa instalasi Node.js dan Appium."
            )
        else:
            msg = (
                "Appium tidak terinstal di komputer ini.\n"
                "Cara instalasi:\n"
                "  npm install -g appium\n"
                "  appium driver install uiautomator2\n"
                "Atau kunjungi: http://appium.io"
            )
        print(msg, file=sys.stderr)
        sys.exit(1)

    version = get_appium_version()
    print(f"Memulai Appium server (versi {version}) pada port {port}...")

    args = ["--port", str(port), "--base-path", base_path]
    if log_path:
        args.extend(["--log", str(log_path)])

    _service = AppiumService()
    _service.start(args=args)
    _wait_for_server(f"http://localhost:{port}{base_path}", timeout=wait_timeout)
    print(f"Appium server berjalan di http://localhost:{port}{base_path}")
    return _service


def stop_appium_server() -> None:
    global _service
    if _service and _service.is_running:
        _service.stop()
        print("Appium server dihentikan.")
    _service = None




import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.appium_server import start_appium_server as _start_server, stop_appium_server as _stop_server  # noqa: E402
from utils.emulator import ensure_emulator_running as _ensure_emu, stop_avd as _stop_avd  # noqa: E402


class AppiumServerLibrary:
    """Robot Framework library untuk mengelola Appium server dan emulator."""

    ROBOT_LIBRARY_SCOPE = "SUITE"

    def start_appium_server(self, port: int = 4723, base_path: str = "/wd/hub"):
        log_dir = Path(os.getenv("ROBOT_OUTPUT_DIR", "results"))
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / "appium-server.log"
        _start_server(port=port, base_path=base_path, log_path=log_path)

    def stop_appium_server(self):
        _stop_server()

    def start_android_emulator(self, avd_name: str | None = None, boot_timeout: int = 120, headless: bool = False):
        serial = _ensure_emu(avd_name=avd_name, boot_timeout=boot_timeout, headless=headless)
        return serial

    def stop_android_emulator(self):
        _stop_avd()

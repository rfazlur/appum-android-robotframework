import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


def _get_android_sdk() -> Path | None:
    sdk_root = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
    if sdk_root:
        return Path(sdk_root)
    default = Path.home() / "Library" / "Android" / "sdk"
    if default.is_dir():
        return default
    return None


def _find_binary(name: str) -> str | None:
    sdk = _get_android_sdk()
    if sdk:
        subdirs = {"adb": "platform-tools", "emulator": "emulator"}
        candidate = sdk / subdirs.get(name, "") / name
        if candidate.is_file():
            return str(candidate)
    return shutil.which(name)


def list_avds() -> list[str]:
    emulator_path = _find_binary("emulator")
    if not emulator_path:
        print("emulator binary tidak ditemukan. Pastikan Android SDK terinstal.", file=sys.stderr)
        sys.exit(1)
    result = subprocess.run(
        [emulator_path, "-list-avds"],
        capture_output=True, text=True, check=False,
    )
    avds = [a.strip() for a in result.stdout.splitlines() if a.strip()]
    return avds


def list_active_devices() -> list[dict]:
    adb_path = _find_binary("adb")
    if not adb_path:
        print("adb binary tidak ditemukan. Pastikan Android SDK terinstal.", file=sys.stderr)
        sys.exit(1)
    result = subprocess.run(
        [adb_path, "devices"],
        capture_output=True, text=True, check=False,
    )
    devices = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("List of") or line == "":
            continue
        parts = line.split("\t")
        if len(parts) == 2:
            serial, state = parts
            if state != "":
                devices.append({"serial": serial, "state": state})
    return devices


def _runnning_avd_serials(devices: list[dict]) -> set[str]:
    return {d["serial"] for d in devices if d["state"] in ("device", "offline")}


def start_avd(
    avd_name: str,
    wait_for_boot: bool = True,
    boot_timeout: int = 120,
    headless: bool = False,
) -> None:
    emulator_path = _find_binary("emulator")
    if not emulator_path:
        print("emulator binary tidak ditemukan.", file=sys.stderr)
        sys.exit(1)

    print(f"Memulai emulator: {avd_name}...")
    cmd = [emulator_path, "-avd", avd_name]
    if headless:
        cmd.extend(["-no-window", "-no-audio"])
    subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if wait_for_boot:
        _wait_for_boot(avd_name, timeout=boot_timeout)


def _wait_for_boot(avd_name: str, timeout: int = 120) -> None:
    adb_path = _find_binary("adb")
    deadline = time.time() + timeout

    print("Menunggu emulator terhubung ke ADB...")
    while time.time() < deadline:
        devices = list_active_devices()
        if any(d["state"] == "device" for d in devices):
            break
        time.sleep(2)
    else:
        print("Emulator tidak terhubung dalam batas waktu.", file=sys.stderr)
        sys.exit(1)

    print("Menunggu sistem boot selesai...")
    while time.time() < deadline:
        result = subprocess.run(
            [adb_path, "shell", "getprop", "sys.boot_completed"],
            capture_output=True, text=True, check=False,
        )
        if result.stdout.strip() == "1":
            print(f"Emulator {avd_name} siap digunakan.")
            return
        time.sleep(3)
    print(f"Emulator {avd_name} tidak selesai booting dalam {timeout} detik.", file=sys.stderr)
    sys.exit(1)


def ensure_emulator_running(
    avd_name: str | None = None,
    boot_timeout: int = 120,
    headless: bool = False,
) -> str:
    devices = list_active_devices()
    running_serials = _runnning_avd_serials(devices)

    if running_serials:
        serial = next(iter(running_serials))
        print(f"Emulator sudah aktif: {serial}")
        return serial

    avds = list_avds()
    if not avds:
        print("Tidak ada AVD (Android Virtual Device) yang tersedia.", file=sys.stderr)
        sys.exit(1)

    if avd_name:
        if avd_name not in avds:
            print(f"AVD '{avd_name}' tidak ditemukan. Tersedia: {', '.join(avds)}", file=sys.stderr)
            sys.exit(1)
        target = avd_name
    else:
        target = avds[0]
        print(f"AVD tidak ditentukan. Memilih: {target}")

    start_avd(target, wait_for_boot=True, boot_timeout=boot_timeout, headless=headless)

    for d in list_active_devices():
        if d["state"] == "device":
            return d["serial"]

    print("Gagal mendapatkan serial device setelah boot.", file=sys.stderr)
    sys.exit(1)


def stop_avd() -> None:
    adb_path = _find_binary("adb")
    if not adb_path:
        return
    devices = list_active_devices()
    emulators = [d for d in devices if d["serial"].startswith("emulator-")]
    if not emulators:
        print("Tidak ada emulator yang berjalan.")
        return
    for emu in emulators:
        serial = emu["serial"]
        print(f"Menghentikan emulator: {serial}...")
        subprocess.run(
            [adb_path, "-s", serial, "emu", "kill"],
            capture_output=True, text=True, timeout=10,
        )
    print("Semua emulator dihentikan.")




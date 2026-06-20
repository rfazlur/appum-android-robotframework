# AGENTS.md — appium-robotframework-android

## Purpose

Mobile Android automation testing using **Appium** + **Robot Framework** + **Python**.

## Project structure

```
├── apps/                 # Place APK files here (gitignored)
├── results/              # Test output, screenshots (gitignored)
├── resources/
│   ├── keywords.robot            # Shared AppiumLibrary keywords
│   ├── variables.yaml            # Device, app, and Appium server config
│   └── AppiumServerLibrary.py    # RF library for server lifecycle
├── tests/
│   └── example.robot             # Sample test suite
├── utils/
│   ├── __init__.py
│   ├── appium_server.py          # Server start/stop + install check
│   └── emulator.py               # Emulator detection, start, boot wait
├── requirements.txt
└── AGENTS.md
```

## Setup

```bash
pip install -r requirements.txt
```

Dependencies: `robotframework`, `robotframework-appiumlibrary`, `Appium-Python-Client`, `PyYAML`.

Prerequisites:
- Appium CLI installed: `npm install -g appium && appium driver install uiautomator2`
- Android emulator AVD created (via Android Studio or `avdmanager`)
- APK placed in `apps/` (update path in `resources/variables.yaml`)

## Commands

| Action | Command |
|---|---|
| Run all tests | `robot tests/` |
| Run single file | `robot --outputdir results/ tests/example.robot` |
| Run by tag | `robot --include smoke --outputdir results/ tests/` |

## Appium server

Appium is started/stopped **programmatically** by the test suite — no need to run it manually.

- `Suite Setup` calls `Start Appium Server` then `Open Test App`.
- `Suite Teardown` calls `Close Test App` then `Stop Appium Server`.
- If `appium` CLI is not found, the suite exits immediately with an install guide.

## Emulator

Emulator is also managed programmatically. `Start Android Emulator` (called first in setup):

- Lists available AVDs via `emulator -list-avds`.
- If an AVD is already running, returns its serial.
- If none is running, auto-selects the first AVD (or the one in `variables.yaml`), boots it, and waits for `sys.boot_completed`.

## Conventions

- **Config**: Device, app, and Appium settings in `resources/variables.yaml` — update this first.
- **Keywords**: Reusable Appium interactions in `resources/keywords.robot`.
- **Server URL**: `http://localhost:4723/wd/hub` (Appium started with `--base-path /wd/hub`).
- **Locators**: Prefer `accessibility_id` (Android `content-desc`) for stable selectors.
- **Results**: Always use `--outputdir results/` to keep output clean.
- **YAML variables**: Loaded with `Variables` (not `Resource`) — Robot Framework does not parse `.yaml` as a resource.

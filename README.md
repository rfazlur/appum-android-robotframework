# Appium RobotFramework Android

Automation testing untuk aplikasi Android menggunakan **Appium**, **Robot Framework**, dan **Python**.

Appium server dan emulator dikelola secara otomatis oleh test suite — tidak perlu menjalankan secara manual.

---

## Precondition

Sebelum menjalankan project, pastikan semua prerequisite berikut sudah terpenuhi.

### 1. Appium CLI

```bash
npm install -g appium
appium driver install uiautomator2
```

Cek instalasi:

```bash
appium --version
```

### 2. Android SDK

Android SDK wajib terinstal dan environment variable `ANDROID_HOME` atau `ANDROID_SDK_ROOT` harus diset.

Di macOS (path default):

```bash
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator
```

Cek instalasi:

```bash
adb --version
emulator -list-avds
```

### 3. Emulator Android

Minimal satu AVD (Android Virtual Device) harus tersedia. Buat AVD baru jika belum ada:

**Via Android Studio:** Tools → Device Manager → Create Device

**Via command line:**

```bash
avdmanager create avd -n pixel_9 -k "system-images;android-35;google_apis;arm64-v8a"
```

Cek daftar AVD:

```bash
emulator -list-avds
```

### 4. APK

Letakkan file APK yang akan di-test ke dalam folder `apps/`.

---

## Project Structure

```
.
├── apps/                         # Letakkan APK di sini (gitignore)
├── results/                      # Output test, screenshot, log (gitignore)
├── resources/
│   ├── keywords.robot            # Keyword Robot Framework untuk interaksi dengan Appium
│   ├── variables.yaml            # Konfigurasi device, app, dan Appium server
│   └── AppiumServerLibrary.py    # Library Python untuk lifecycle server & emulator
├── tests/
│   └── login.robot               # Test case: login, logout, & negative login
├── utils/
│   ├── __init__.py
│   ├── appium_server.py          # Start/stop Appium server + health check
│   └── emulator.py               # Deteksi & boot emulator, tunggu device ready
├── requirements.txt              # Dependensi Python
└── README.md
```

---

## Setup

Instal dependensi Python:

```bash
pip install -r requirements.txt
```

---

## Konfigurasi

Semua konfigurasi ada di `resources/variables.yaml`:

```yaml
app:
  path: ${CURDIR}/../apps/Android-MyDemoAppRN.1.3.0.build-244.apk
  package: com.saucelabs.mydemoapp.rn
  activity: com.saucelabs.mydemoapp.rn.MainActivity
  waitActivity: com.saucelabs.mydemoapp.rn.MainActivity

device:
  platformName: Android
  platformVersion: "16"
  deviceName: Android Emulator
  automationName: UiAutomator2

emulator:
  avdName:
  bootTimeout: 120
  headless: false

appium:
  server: http://localhost:4723/wd/hub
  implicitWait: 10
  newCommandTimeout: 300
```

Sesuaikan `app.path`, `app.package`, `app.activity`, dan `device.platformVersion` dengan aplikasi yang akan di-test.

---

## Menjalankan Test

### Semua test

```bash
robot tests/
```

### Satu file

```bash
robot --outputdir results/ tests/login.robot
```

### Satu test case (by name)

```bash
robot --test "Login - Negative Invalid Credentials" --outputdir results/ tests/login.robot
```

### Filter by tag

```bash
robot --include smoke --outputdir results/ tests/
```

---

## Test Files

| File | Test Cases | Deskripsi |
|---|---|---|
| `login.robot` | 3 | **Login** (bob@example.com), **Logout** (dengan konfirmasi dialog), **Negative Login** (invalid credentials → error message) |

### Detail Test Cases (login.robot)

| Test Case | Langkah | Verifikasi |
|---|---|---|
| **Success Login** | Hamburger → Log In → input email & password → klik Login | Halaman Products muncul |
| **Success Logout** | Hamburger → Log Out → konfirmasi LOG OUT → OK | Hamburger menampilkan Log In |
| **Negative Invalid Credentials** | Hamburger → Log In → input email/password salah → klik Login | Error *"Provided credentials do not match any user in this service."* |

## Key Locators (Sauce Labs My Demo App RN)

| Elemen | Locator |
|---|---|
| Hamburger menu | `accessibility_id=open menu` |
| Log In (menu) | `accessibility_id=menu item log in` |
| Log Out (menu) | `accessibility_id=menu item log out` |
| Username field | `accessibility_id=Username input field` |
| Password field | `accessibility_id=Password input field` |
| Login button | `accessibility_id=Login button` |
| Products label | `xpath=//android.widget.TextView[@text="Products"]` |
| Login error | `xpath=//android.widget.TextView[@text="Provided credentials do not match any user in this service."]` |
| Logout confirm | `xpath=//android.widget.Button[@text="LOG OUT"]` |
| Logout success OK | `xpath=//android.widget.Button[@text="OK"]` |

## Alur Eksekusi

Test suite menjalankan semua langkah secara otomatis:

```
Suite Setup →
  1. Start Android Emulator  (deteksi AVD, boot jika belum nyala)
  2. Start Appium Server     (cek instalasi, start server, health check)
  3. Open Test App           (install & buka aplikasi via Appium)

Test Cases →
  4. [test]                  (interaksi dengan aplikasi)

Suite Teardown →
  5. Close Test App          (screenshot, tutup sesi Appium)
  6. Stop Appium Server      (stop server)
  7. Stop Android Emulator   (matikan emulator)
```

Jika Appium CLI belum terinstal, test suite akan berhenti dengan pesan error dan panduan instalasi. Begitu juga jika tidak ada AVD yang tersedia.
# appum-android-robotframework
# appum-android-robotframework

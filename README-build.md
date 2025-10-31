Smart Budget Manager - Build Instructions (simple)

This archive contains the app source and a buildozer.spec template to build an Android APK on Linux (recommended) or WSL2 (Windows). I cannot build the APK for you from here, but these steps will create the APK on your computer.

Quick steps (WSL2 / Ubuntu recommended):

1) Install WSL2 (Windows) or use a Linux machine (Ubuntu/Debian).
   - For WSL2 on Windows: run in PowerShell (Admin): wsl --install
   - Open Ubuntu and set up your user.

2) Install system requirements in Ubuntu:
   sudo apt update && sudo apt install -y python3-pip python3-venv git zip unzip openjdk-11-jdk build-essential        libssl-dev libffi-dev libsqlite3-dev zlib1g-dev liblzma-dev libbz2-dev android-tools-adb

3) Create venv & install Python packages:
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install cython==0.29.33
   pip install buildozer
   pip install -r requirements.txt

4) Initialize buildozer (if not already):
   buildozer init
   # if using the provided buildozer.spec, you can skip editing

5) Build the APK (first run downloads Android SDK/NDK, may take ~30-60 minutes):
   buildozer -v android debug

6) After success, APK will be in bin/ directory (e.g., bin/smartbudget-0.1-debug.apk).
   Use adb install bin/smartbudget-0.1-debug.apk or copy to your phone.

Notes & troubleshooting:
- If build fails, copy the terminal error and share it with me; I'll explain how to fix it.
- On Windows, use WSL2 — building natively on Windows is more complex.
- You can also use a cloud CI (GitHub Actions) to build if you prefer not to use your machine. I can provide a GitHub Actions workflow file on request.

If you want, I can now guide you step-by-step while you run these commands on your computer and help fix any errors that appear.

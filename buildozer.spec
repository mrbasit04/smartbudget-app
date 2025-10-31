[app]
title = Smart Budget Manager
package.name = smartbudget
package.domain = org.smartbudget
source.dir = .
source.include_exts = py,png,kv,txt
version = 0.1
orientation = portrait
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (list) Application requirements
requirements = python3,kivy,kivymd,matplotlib,sqlite3

# (str) Android entry point, default is ok
# entrypoint = main.py

# (int) Target API
android.api = 31

# (str) Android NDK version to use (if omitted, will be selected)
# android.ndk = 23b

# (list) Supported orientation
orientation = portrait

# (str) Presplash image path (optional)
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (list) Add permissions
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (str) Supported architectures
android.arch = armeabi-v7a, arm64-v8a

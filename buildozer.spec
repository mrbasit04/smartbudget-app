[app]
# (str) Title of your application
title = SmartBudget Manager

# (str) Package name
package.name = smartbudgetmanager

# (str) Package domain (unique identifier)
package.domain = org.smartbudget

# (str) Source code directory
source.dir = .

# (list) Include these file extensions in your app
source.include_exts = py,png,jpg,kv,atlas,db,sqlite3

# (str) Application versioning (method 1)
version = 1.0

# (str) Application orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (str) Entry point of your application
entrypoint = SmartBudgetManager_app.py

# (str) Application icon (optional)
# icon.filename = icons/app_icon.png

# (list) Supported orientations
android.orientation = portrait

# (str) Android API level
android.api = 33

# (str) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Indicate if you want to include SQLite3
sqlite3 = 1

# (list) Application requirements
requirements = python3, kivy, kivymd, sqlite3, pandas, matplotlib

# (str) Command to run when starting the app
# Uncomment the next line if your main file has a different name
# main.py is not needed since entrypoint handles it
# run = SmartBudgetManager_app.py

# (bool) Hide the title bar
android.hide_titlebar = 0

# (str) The format used to package the app
package.format = apk

# (bool) Presplash
# android.presplash = true

# (str) Presplash color or image
# android.presplash_color = #FFFFFF

# (list) Services to include (if any)
services =

# (list) Garden requirements (if you use KivyMD or extra widgets)
# garden_requirements =

# (str) Logcat filters to show (useful for debugging)
log_level = 2

# (str) Android entrypoint (default is fine)
android.entrypoint = org.kivy.android.PythonActivity

# (bool) Copy library instead of symlink
copy_libs = 1

# (bool) Strip debug symbols
android.strip_debug = 1

# (str) Build directory (default is fine)
build_dir = .buildozer

# (str) Name of the output APK
android.arch = armeabi-v7a

# (str) Orientation mode (portrait or landscape)
orientation = portrait

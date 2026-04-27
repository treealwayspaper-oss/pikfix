# 📦 Packaging Guide for PikFix

This guide explains how to turn the PikFix source code into a standalone executable (`.exe` for Windows or `.app` for macOS).

## 🛠️ Prerequisites

You must perform these steps on the OS you are targeting (e.g., use Windows to create a `.exe`).

1. **Install Python 3.9+**
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

## 🚀 Building the Executable

We use a `.spec` file to ensure all assets and dependencies are correctly bundled.

### 🪟 For Windows (.exe)
1. Open Terminal/CMD in the `pikfix` root folder.
2. Run the following command:
   ```bash
   pyinstaller pikfix.spec
   ```
3. Once completed, your standalone executable will be located in the **`dist/`** folder.

### 🍎 For macOS (.app)
1. Open Terminal in the `pikfix` root folder.
2. Run the following command:
   ```bash
   pyinstaller pikfix.spec
   ```
3. Your `.app` bundle will be located in the **`dist/`** folder.

---

## 🔍 Troubleshooting

### "ModuleNotFoundError" after launch
If the app crashes saying a module is missing, it means PyInstaller didn't automatically detect a hidden dependency. You can add it to the `hiddenimports` list in `pikfix.spec` and run the build command again.

### Reducing File Size
The resulting binary can be large because it includes the entire PySide6 runtime. To reduce the size, you can:
1. Use a clean virtual environment (venv) to build.
2. Install `upx` on your system, and PyInstaller will automatically compress the binary.

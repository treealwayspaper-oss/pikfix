# 🚀 PikFix Setup & Execution Guide

This guide provides instructions on how to set up the local environment and run the PikFix application on your machine.

## 🛠️ Prerequisites
- **Python 3.9 or higher** installed on your system.
- **Git** (optional, if you are cloning the repo).

## 📦 Local Environment Setup (Recommended)

To avoid conflicts with other Python projects, it is strongly recommended to use a virtual environment.

### 🪟 Windows
1. Open Terminal or Command Prompt in the `pikfix` folder.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
   .\venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 🍎 macOS / 🐧 Linux
1. Open Terminal in the `pikfix` folder.
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🏃 How to Run the Application

Once the environment is set up and activated, run the following command:

```bash
python src/main.py
```

## 🧪 Testing the Logic (Optional)
If you want to verify that the data matching logic is working correctly without opening the UI, you can run the logic test script:

```bash
# Ensure you are in the pikfix root directory
python -m tests.test_data_loader
```

## 📦 Packaging into Executable (.exe / .app)
*(This will be provided in a later stage. We will use PyInstaller or Nuitka to create a standalone binary.)*

# 📖 PikFix User Guide

Welcome to **PikFix**, a professional tool for AI training data review and Ground Truth (GT) selection.

## 🚀 Getting Started

1. **Environment Setup**: Follow the instructions in `SETUP.md` to install dependencies and run the application.
2. **Data Configuration**:
    - **Root Path**: Select the folder that contains all your image subfolders.
    - **Source Folder**: Select the folder containing the original images.
    - **Candidate Folders**: Select one or more folders containing the potential GT images.
    - Click **"Load Images and Start Review"** to begin.

## 🖼️ How to Review

### Interface Overview
- **Left Side**: The **Source Image** is displayed.
- **Right Side**: All matched **Candidate GT images** are displayed in a dynamic grid.
- **Top**: Shows your current progress (e.g., "Reviewing 10 / 500").
- **Bottom**: Navigation and Action buttons.

### Selection & Saving
1. Compare the Source image with the Candidates.
2. Select the best candidate by clicking the **"Select as GT"** radio button.
3. Click **"Save Selected GT"** to confirm. The image will be saved to the `final_gt` folder in your root directory.

---

## ⌨️ Keyboard Shortcuts (Power User Mode)

To process large datasets efficiently, use the following shortcuts:

| Key | Action | Description |
| :--- | :--- | :--- |
| `⬅️` (Left Arrow) | **Previous** | Move to the previous image set. |
| `➡️` (Right Arrow) | **Next** | Move to the next image set. |
| `1` ~ `9` | **Quick Select** | Instantly select the $N$-th candidate in the grid. |
| `Enter` / `S` | **Save & Next** | Save the selected GT and automatically move to the next image. |

---

## 🔄 Resume Feature

PikFix automatically saves your progress. If you close the program and restart it, it will **automatically load the last image you were reviewing**, allowing you to pick up exactly where you left off.

- Progress is stored in `review_progress.json` in your root data folder.
- To start from the beginning, simply delete the `review_progress.json` file.

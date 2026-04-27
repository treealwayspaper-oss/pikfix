# 📜 PikFix Development Changelog

This document tracks the evolution of the PikFix project from initialization to the current version.

## 🛠️ Milestone 1: Project Foundation & Core Logic
**Focus**: Defining specifications and implementing the data matching engine.

- **Specifications**: Defined the AI training data review goal and established the "Stem-based matching" logic (matching files by name regardless of extension).
- **Tech Stack**: Selected **PySide6** as the GUI framework to ensure cross-platform compatibility and the ability to package as a standalone executable (`.exe`, `.app`).
- **Architecture**: Established a professional folder structure (`src/core`, `src/ui`, `docs`, `tests`).
- **Data Loader**: Implemented `DataLoader` to handle directory scanning and image pairing.
- **Verification**: Created an automated logic test suite in `tests/test_data_loader.py` to ensure matching accuracy.
- **Documentation**: Created `docs/specifications.md` and `SETUP.md`.

## 🖼️ Milestone 2: Review Interface & Core Workflow
**Focus**: Building the visual environment for data curation.

- **Setup UI**: Implemented the initial configuration screen for root path and folder selection.
- **Review Window**: Developed the main `ReviewWindow` to display source vs. candidate images.
- **Dynamic Grid**: Implemented an auto-calculating grid layout (e.g., 2x2, 3x3) that adapts to the number of candidates.
- **UX Optimization**: 
    - Removed scroll areas to fit all candidates on one screen.
    - Adjusted layout stretch factors to prioritize the visibility of candidate images over the source.
- **Save Logic**: Implemented the GT saving mechanism (copying selected images to `final_gt` folder).

## ⌨️ Milestone 3: Productivity & State Management
**Focus**: Improving work efficiency for large-scale datasets.

- **Resume Feature**: Implemented `ProgressManager` using `review_progress.json` to allow users to pick up work where they left off.
- **Keyboard Shortcuts**: Added "Power User" shortcuts:
    - `Left/Right Arrows`: Fast navigation.
    - `1-9` keys: Instant candidate selection.
    - `Enter/S` keys: One-click save and next.
- **User Documentation**: Created `USER_GUIDE.md` to help users leverage these efficiency features.

## 🔍 Milestone 4: Precision Review Tools
**Focus**: Enhancing the ability to detect fine details in images.

- **High-Res Detail Window**: Implemented `ImageDetailWindow` for deep inspection.
- **Zoom & Pan**: Added mouse-wheel zooming and scroll-based panning for high-resolution review.
- **Interactive Triggers**: Implemented double-click signals on all images to instantly open the detail view.
- **Dynamic Scaling**: Introduced `DynamicImageLabel` to ensure images scale perfectly with the window size while maintaining aspect ratio.

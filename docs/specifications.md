# pikfix - Requirements & Specifications

## 🎯 Project Goal
Develop a tool for reviewing and processing training data for AI model development. The primary purpose is to compare a source image with multiple candidate Ground Truth (GT) images and select the most appropriate one to be saved as the final GT.

## ⚙️ Operational Constraints
- **Execution Environment**: Standalone Desktop Application (Not a web service).
- **Distribution**: Must be packaged as a single executable binary (e.g., `.exe` for Windows, `.app` for macOS).
- **Connectivity**: Must be fully functional offline (no external internet required after setup).
- **Cross-Platform**: Must run on Windows, Ubuntu, and macOS.
- **UI Flexibility**: The interface must dynamically adapt to the number of candidate GT folders provided by the user.

## 📂 Data Structure
- **Root Directory**: Contains multiple subdirectories (e.g., `source`, `haze`, `low`, etc.).
- **Folder Configuration**:
    - **Source Folder**: The user selects one folder to be defined as the source of truth (Original images).
    - **Candidate Folders**: The user selects one or more folders containing potential GT images.
- **Image Matching Logic**:
    - Matching is based on the **filename (stem)**, ignoring the file extension.
    - *Example*: `source/image1.jpg`, `haze/image1.png`, and `low/image1.jpg` are all treated as the same data point (`image1`).

## 💻 Technical Stack
- **Language**: Python 3.x
- **GUI Framework**: PySide6 (Official Qt for Python)
- **Packaging**: PyInstaller / Nuitka (for .exe and .app)
- **Libraries**: Pillow (PIL) for image handling

## 🛠️ Functional Requirements
1. **Configuration Interface**:
    - Input for the data root path.
    - Dynamic listing of subfolders for selecting the Source folder and Candidate folders.
2. **Data Loader**:
    - Scan selected folders and group files by their stem.
    - Create a mapping: `Source Image` $\rightarrow$ `[Candidate Image 1, Candidate Image 2, ... Candidate Image N]`.
3. **Comparison UI**:
    - Display the source image and all matched candidate images on a single screen for easy comparison.
    - The layout must adjust dynamically based on the number of selected candidate folders.
    - **Dynamic Sizing**: Images should scale based on window size while maintaining aspect ratio.
4. **Selection & Storage**:
    - Allow the user to select one candidate as the final GT.
    - Save the selected candidate to a designated output folder.
    - **Keyboard Shortcuts**: Support for navigation (`Arrows`), selection (`1-9`), and saving (`Enter/S`).
5. **Workflow Management**:
    - Navigation to move to the next image pair.
    - Progress tracking (processed vs. total images).
    - **Resume Feature**: Automatically save and load current progress from a file.

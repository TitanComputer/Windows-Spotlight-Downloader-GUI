# 💻 Windows Spotlight Downloader (GUI Edition)

A simple graphical interface for downloading and managing Windows Spotlight images.

It scrapes the current Spotlight images and stores them locally, avoiding duplicates using a persistent state file.

> This project has been compiled into an executable (`.exe`) using **auto-py-to-exe** for easy distribution on Windows systems.

> **Looking for the CLI version?**  
> 👉 [Check out the original CLI repository here](https://github.com/TitanComputer/Windows-Spotlight-Downloader)


## 🚀 Features

- Downloads high-quality Windows Spotlight wallpapers
- Separates and saves images into Landscape and Portrait folders
- Allows users to select download mode (Landscape only / Portrait only / Both)
- Easy-to-use graphical interface built with `ttkbootstrap`
- Portable `.exe` version included (no Python required)
- Supports Windows 10 & 11
- Robust internet error handling — retries failed pages instead of skipping
- Avoids re-downloading previously saved images
- Stores execution state in a local JSON file
- Simple, lightweight, and fast — no bloat

## 🖼️ Screenshots

Coming soon...

## 📥 Download

You can download the latest compiled `.exe` version from the [Releases](https://github.com/TitanComputer/windows-spotlight-downloader-GUI/releases/latest) section.  
No need to install Python — just download and run.

## ⚙️ Usage

If you're using the Python script:
```bash
python Windows-Spotlight-Downloader-GUI.py
```
Or, run the Windows-Spotlight-Downloader-GUI.exe file directly if you downloaded the compiled version.

Once the application is running, follow these steps:

Choose the download mode using the radio buttons:

🔘 Landscape only – to download only horizontal (wide) images

🔘 Portrait only – to download only vertical images

🔘 Both – to download all image types

Click the Start button to begin downloading.

The program will then begin downloading images based on your selection.

Save new images to the selected folder and Skip any duplicates using the internal state.json tracking

If a network error occurs, it will retry the page until all images are successfully downloaded.

Tip: You can customize download paths by editing Windows-Spotlight-Downloader-GUI.py if you are running from the source code.

## 📦 Dependencies

- Python 3.9 or newer
- `ttkbootstrap`

Standard libraries only (os, json, datetime, etc.)

If you're modifying and running the script directly and use additional packages (like requests or beautifulsoup4), install them via:
```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```bash
windows-spotlight-downloader-gui/
│
├── Windows-Spotlight-Downloader-GUI.py     # Main launcher
├── gui_module.py                     # GUI components and logic
├── state.json                  # Auto-generated to track previously downloaded images
├── Windows-Spotlight-Downloader-GUI.exe    # Optional standalone executable
├── Downloads/
│   ├── Landscape/              # Landscape-oriented images
│   └── Portrait/               # Portrait-oriented images
├── requirements.txt            # Dependencies
└── README.md                   # Project documentation
```
## ❓ What is Windows Spotlight?

Windows Spotlight is a feature in Windows 10 and 11 that automatically displays beautiful, high-resolution images on the lock screen.  
These images are curated by Microsoft and often feature landscapes, architecture, and other stunning visuals.  

However, the images are not directly accessible or downloadable through the standard Windows interface — this tool helps you fetch and save them locally in an organized way.

## 🌐 Source of Images and Legal Notice
This tool downloads images from windows10spotlight.com, a third-party archive of Windows Spotlight wallpapers.
All images are originally provided by Microsoft through Windows Spotlight.

Legal Note: All images remain the property of Microsoft. This project is for educational and personal use only.
Please respect the copyrights of both Microsoft and windows10spotlight.com, which curates the image collection.

## 🛠 Compiled with auto-py-to-exe
This project was packaged into a standalone .exe using auto-py-to-exe.
This allows users to run the program without needing to install Python.

## 🤝 Contributing
Pull requests are welcome.
If you have suggestions for improvements or new features, feel free to open an issue.

## ☕ Support
If you find this project useful and would like to support its development, consider donating:
## 💰 USDT (Tether) – TRC20 Wallet Address:

```bash
TGoKk5zD3BMSGbmzHnD19m9YLpH5ZP8nQe
```
Thanks a lot for your support! 🙏

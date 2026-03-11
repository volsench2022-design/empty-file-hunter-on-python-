# Empty File Hunter

<img width="952" height="663" alt="Screenshot 2026-03-11 173553" src="https://github.com/user-attachments/assets/78d438e2-c897-41f0-b33b-5976760be7d8" />


**Empty File Hunter** is a simple desktop application built with **Python** and **CustomTkinter** that scans directories and finds empty folders. It allows users to quickly locate unused directories and optionally remove them to keep their file system clean.

## Features

* 📂 Select any folder on your system to scan
* 🔎 Recursively scans all subdirectories
* 🗑 Detects empty folders automatically
* ⚡ Option to delete all detected empty folders with confirmation
* 🖥 Simple and modern graphical interface using CustomTkinter
* 🚫 Ignores system directories like `$RECYCLE.BIN` and `System Volume Information`

## How It Works

1. Click **Select Folder** to choose a directory.
2. Press **Scan** to search for empty folders.
3. The application lists all empty directories found.
4. Click **Clean All** to remove them (after confirmation).

## Requirements

* Python 3.9+
* customtkinter

Install the required dependency:

```
pip install customtkinter
```

## Running the Application

Run the script directly:

```
python empty_file_hunter.py
```

## Interface Overview

* **Select Folder** – choose the directory to scan
* **Scan** – search for empty folders
* **Clean All** – delete all detected empty folders
* **Results Box** – displays the list of empty directories found
* **Status Bar** – shows the total number of empty folders detected

## Notes

* The application skips certain system folders to avoid permission errors.
* Deleting folders is irreversible, so the program asks for confirmation before removing them.

## License

This project is intended for educational and personal use.

# Manual-Data-Processor-for-a-VPS
The script automates the retrieval of media assets by processing a JSON block provided via standard input. It handles two primary tasks
# Subz Downloader

A lightweight Python script designed to automate the process of downloading subtitles and movie content from [subz.lk](https://subz.lk/). This tool is optimized for use on a VPS/headless server environment where you provide media data via a JSON input.

---

## Features

* **Automated Subtitle Extraction**: Automatically downloads ZIP files, extracts `.srt` files, and saves them locally.
* **Torrent Integration**: Supports both magnet links and `.torrent` files for downloading media content.
* **Real-time Progress Monitoring**: Displays download percentage, transfer speed, peer count, and current status directly in the terminal.
* **Input Handling**: Designed to process JSON data pasted directly into the terminal, making it easy to use via SSH/PuTTY.

## Prerequisites

This script requires the `libtorrent` library to handle BitTorrent downloads. You can install it on your system using:

```bash
sudo apt install python3-libtorrent

```

## How to Use

1. Run the script: `python3 subz_downloader.py`.
2. When prompted, paste your JSON data block into the terminal.
3. Press **ENTER** and then **CTRL+D** to signal the end of input.

**Expected JSON Format:**
Ensure your JSON contains the following keys:

* `title`: The name of the movie.
* `sinhala_sub_link`: Direct link to the subtitle ZIP file.
* `torrent_720p`, `torrent_link`, or `torrent_yts`: The link to the torrent/magnet file.

## Safety Features

* **Filename Sanitization**: The script automatically removes invalid characters (e.g., `\/*?:"<>|`) from the movie title to prevent file system errors.
* **Timeout Protection**: Network requests are capped with a 30-second timeout to prevent the script from hanging.

---

*Note: This script is intended for use in environments where you have the necessary permissions to download and store media files.*

Would you like any adjustments to the error handling or logging features of this script?

# MP3 Song Renamer with ACRCloud API

This Python script **automatically identifies MP3 files** using the [ACRCloud API](https://www.acrcloud.com/) and renames them based on the identified song title. The script also organizes songs into separate folders for recognized and unrecognized tracks, making it easier to manage your music library.

---

## Features

- 🔍 **Identifies songs** by sending audio samples to the ACRCloud API.
- 📝 **Renames MP3 files** based on the identified song title.
- 🚫 **Removes metadata** from renamed MP3 files.
- ⚙️ Handles **corrupt or unrecognizable MP3 files** by attempting re-encoding.
- 🗂️ **Organizes files** into two folders:
  - `renamed_songs`: For successfully identified and renamed songs.
  - `unreg_songs`: For songs that could not be identified.

---

## Prerequisites

### Python
- **Python 3.8** or higher is required.

### ACRCloud API
- You need a valid [ACRCloud API](https://www.acrcloud.com/) account to obtain:
  - `access_key`
  - `access_secret`
  - `requrl` (host URL).

### FFmpeg
- You must have **FFmpeg** installed on your system:
  - Download from [FFmpeg.org](https://ffmpeg.org/download.html).
  - Follow the installation instructions based on your OS.
  - Make sure to **add FFmpeg to your system's PATH**.

---

## Installation

### 1. Clone the Repository
Start by cloning the repository to your local machine:
```bash
git clone https://github.com/Kav36/mp3-renamer.git

# MP3 Song Renamer with ACRCloud API

This Python script automatically identifies MP3 files using the [ACRCloud API](https://www.acrcloud.com/) and renames them based on the identified song title. It also organizes songs into separate folders for recognized and unrecognized tracks.

---

## Features
- Identifies songs by sending audio samples to the ACRCloud API.
- Renames MP3 files based on the identified song title.
- Removes metadata from renamed MP3 files.
- Handles corrupt or unrecognizable MP3 files by attempting re-encoding.
- Organizes files into:
  - `renamed_songs`: For successfully identified and renamed songs.
  - `unreg_songs`: For songs that could not be identified.

---

## Prerequisites

### Python
- Python 3.8 or higher.

### ACRCloud API
- A valid [ACRCloud API](https://www.acrcloud.com/) account to obtain:
  - `access_key`
  - `access_secret`
  - `requrl` (host URL).

### FFmpeg
- `ffmpeg` installed on your system:
  - Download it from [FFmpeg.org](https://ffmpeg.org/download.html).
  - Follow the installation instructions for your operating system.
  - Add the `ffmpeg` binary to your system's PATH.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/mp3-renamer.git
cd mp3-renamer

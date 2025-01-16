# Kavindu Madulakshan © 2025 MP3 Renamer. All rights reserved.

import base64
import hashlib
import hmac
import os
import time
import requests
from pydub import AudioSegment
import shutil
import re
from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError
import subprocess

# Replace with your actual credentials and host
access_key = "###YOUR_ACCESS_KEY###"
access_secret = "###YOUR_ACCESS_SECRET###"
requrl = "https://###HOST###/v1/identify"

# ACRCloud signature generation constants
http_method = "POST"
http_uri = "/v1/identify"
data_type = "audio"
signature_version = "1"
timestamp = time.time()

# Creating the signature string
string_to_sign = (
    f"{http_method}\n{http_uri}\n{access_key}\n{data_type}\n{signature_version}\n{timestamp}"
)

# Generate signature using HMAC-SHA1
sign = base64.b64encode(
    hmac.new(
        access_secret.encode('ascii'),
        string_to_sign.encode('ascii'),
        digestmod=hashlib.sha1
    ).digest()
).decode('ascii')

# Function to remove metadata from an MP3 file
def remove_metadata(file_path):
    try:
        audio = MP3(file_path)
        audio.delete()
        audio.save()
    except ID3NoHeaderError:
        pass  # No metadata to remove

# Function to send an audio chunk to the ACRCloud API
def send_to_acrcloud(file_path):
    sample_bytes = os.path.getsize(file_path)

    files = [
        ('sample', (os.path.basename(file_path), open(file_path, 'rb'), 'audio/mpeg'))
    ]
    data = {
        'access_key': access_key,
        'sample_bytes': sample_bytes,
        'timestamp': str(timestamp),
        'signature': sign,
        'data_type': data_type,
        'signature_version': signature_version
    }

    response = requests.post(requrl, files=files, data=data)
    response.encoding = "utf-8"
    return response.json()

# Function to clean the song name (remove anything in parentheses)
def clean_song_name(song_name):
    return re.sub(r'\s?\(.*\)', '', song_name).strip()

# Function to sanitize filenames (remove invalid characters)
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

# Function to re-encode an MP3 file using FFmpeg
def reencode_mp3(file_path, output_path):
    command = [
        'ffmpeg', '-i', file_path, '-acodec', 'libmp3lame', '-ar', '44100', '-ab', '192k', output_path
    ]
    try:
        subprocess.run(command, check=True)
        print(f"File re-encoded successfully: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error re-encoding file {file_path}: {e}")
        return False

# Main script logic
if __name__ == "__main__":
    # Folder paths
    folder_path = 'C:/Songs_rename/Songs'
    renamed_folder_path = 'C:/Songs_rename/renamed_songs/'
    unreg_folder_path = 'C:/Songs_rename/unreg_songs/'

    # Create output folders if they don't exist
    os.makedirs(renamed_folder_path, exist_ok=True)
    os.makedirs(unreg_folder_path, exist_ok=True)

    # Iterate over MP3 files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp3"):
            file_path = os.path.join(folder_path, filename)

            try:
                # Load the audio file using pydub
                audio = AudioSegment.from_mp3(file_path)
            except Exception as e:
                print(f"Error loading audio file {filename}: {str(e)}")
                temp_file_path = os.path.join(folder_path, f"fixed_{filename}")
                if reencode_mp3(file_path, temp_file_path):
                    file_path = temp_file_path
                else:
                    print(f"Skipping {filename} due to decoding failure.")
                    continue

            # Extract a 30-second chunk after skipping the first 10 seconds
            chunk_audio = audio[10000:40000]
            temp_chunk_path = "temp_chunk.mp3"
            chunk_audio.export(temp_chunk_path, format="mp3")

            # Send the audio chunk to the ACRCloud API
            response = send_to_acrcloud(temp_chunk_path)

            if response.get("status", {}).get("code") == 2004:
                print(f"Fingerprint generation failed for {filename}.")
                temp_file_path = os.path.join(folder_path, f"reencoded_{filename}")
                if reencode_mp3(file_path, temp_file_path):
                    response = send_to_acrcloud(temp_file_path)
                    if response.get("status", {}).get("code") != 2004:
                        file_path = temp_file_path
                    else:
                        os.remove(temp_file_path)
                        continue
                else:
                    continue

            # If the song is identified, rename and move it
            if 'metadata' in response and 'music' in response['metadata'] and len(response['metadata']['music']) > 0:
                song_name = response['metadata']['music'][0]['title']
                cleaned_song_name = sanitize_filename(clean_song_name(song_name))
                new_file_path = os.path.join(renamed_folder_path, f"{cleaned_song_name}.mp3")
                shutil.move(file_path, new_file_path)
                remove_metadata(new_file_path)
                os.remove(temp_chunk_path)
                print(f"File renamed and moved to {new_file_path}.")
            else:
                # If the song is not identified, move it to the unreg_songs folder
                unreg_file_path = os.path.join(unreg_folder_path, filename)
                shutil.move(file_path, unreg_file_path)
                print(f"Could not identify song for {filename}. Moved to {unreg_file_path}.")

    # Clean up the temporary chunk file
    if os.path.exists("temp_chunk.mp3"):
        os.remove("temp_chunk.mp3")

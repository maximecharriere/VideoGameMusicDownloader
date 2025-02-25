# VideoGameMusicDownloader

A Python script to download music albums from "[Video Game Music](https://downloads.khinsider.com/)" website, for free.

## Credits & Support

- Special thanks to KH Insider for hosting these video game music files and to all uploaders for their valuable contributions ❤
- Consider supporting KH Insider by [upgrading your account](https://downloads.khinsider.com/forums/index.php?account/upgrades) to get direct album downloads.
- Whenever possible, please support the artists by purchasing official soundtracks through legitimate channels.

## Features

- Downloads complete albums including all audio tracks
- Automatically creates organized directories for each album
- Downloads album artwork and cover images
- Saves album information in text files
- Shows download progress for each file
- Validates album URLs before downloading
- Creates safe filenames for all operating systems
- Downloads both MP3 and FLAC formats when available

## Requirements

- Python 3.6 or higher
- Required packages listed in requirements.txt

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/VideoGameMusicDownloader.git
cd VideoGameMusicDownloader
```

2. Install required packages using requirements.txt:
```bash
pip install -r requirements.txt
```

## Usage

Run the script with an album URL from KH Insider:

```bash
python main.py "https://downloads.khinsider.com/game-soundtracks/album/album-name"
```

The script will:
1. Create a directory named after the album
2. Download the album information file
3. Download all album artwork
4. Download all music tracks

## Directory Structure

Downloads are organized as follows:
```
Album Name (Year)/
├── info.txt
├── images/
│   ├── cover.jpg
│   └── other-artwork.jpg
├── track1.mp3
├── track1.flac
├── track2.mp3
├── track2.flac
└── ...
```

## Legal Notice

This tool is for personal use only. Please respect copyright laws and support game composers by purchasing official soundtracks when available.

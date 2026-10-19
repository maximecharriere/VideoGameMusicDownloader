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
- Choose the audio format to download: MP3, FLAC, or both
- Skips tracks that were already downloaded, so an interrupted download can be resumed
- Works with the site's Cloudflare protection by imitating a real Chrome browser (via [curl_cffi](https://github.com/lexiforest/curl_cffi))

## Requirements

- Python 3.10 or higher
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

By default only MP3 files are downloaded. Use `--format` to choose:

```bash
python main.py "https://downloads.khinsider.com/game-soundtracks/album/album-name" --format flac
python main.py "https://downloads.khinsider.com/game-soundtracks/album/album-name" --format all
```

| Option | Downloads |
|---|---|
| `--format mp3` (default) | MP3 files only |
| `--format flac` | FLAC files only (when the album offers them) |
| `--format all` | Every format available for the album |

Albums are saved in a `downloads/` folder by default. Use `-o` / `--output` to choose another root folder:

```bash
python main.py "https://downloads.khinsider.com/game-soundtracks/album/album-name" -o "D:/Music/Game Soundtracks"
```

The script will:
1. Create a directory named after the album, inside the output folder
2. Download the album information file
3. Download all album artwork
4. Download all music tracks, skipping files that already exist

## Directory Structure

Downloads are organized as follows (example with `--format all`):
```
downloads/
└── Album Name (Year)/
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

## Troubleshooting

**`403 Client Error: Forbidden`**: the site is protected by Cloudflare, which blocks requests that don't look like they come from a real browser. Make sure the dependencies are up to date (`pip install -r requirements.txt`) so the script uses `curl_cffi`. If Cloudflare tightens its checks, the 403 may come back even with `curl_cffi`.

## Legal Notice

This tool is for personal use only. Please respect copyright laws and support game composers by purchasing official soundtracks when available.

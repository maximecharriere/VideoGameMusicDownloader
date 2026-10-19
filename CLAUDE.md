# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Single-script scraper (`main.py`) that downloads a full album (info file, artwork, audio tracks) from KH Insider (`downloads.khinsider.com`). There is no build step, test suite, or linter configured.

Follow the conventions in @CODE_PRACTICES.md (code style, error handling, testing, commit granularity).

## Commands

```bash
# Install dependencies (project venv lives in .venv)
.venv/Scripts/python -m pip install -r requirements.txt

# Run (format: mp3 | flac | all, default mp3)
.venv/Scripts/python main.py "https://downloads.khinsider.com/game-soundtracks/album/<album-slug>" --format flac
```

Downloads are written to an `Album Name (Year)/` directory in the **current working directory**. When test-running, `cd` into a temporary directory first so album folders don't land in the repo (only `downloads/` is gitignored).

## Cloudflare protection

The site is behind a Cloudflare managed challenge. Plain `requests` (even with a spoofed User-Agent) gets `403` with `Cf-Mitigated: challenge`. All HTTP traffic must go through the module-level `session = requests.Session(impersonate="chrome")` from `curl_cffi`, which mimics Chrome's TLS fingerprint.
- Don't reintroduce `import requests` or custom `User-Agent` headers; a UA that doesn't match the impersonated fingerprint makes detection more likely.
- Streamed responses (`stream=True`) must be closed explicitly. `download_file` wraps its body in `try/finally: response.close()` for this reason, including the early return when a file already exists.

## Scraping flow

`scrape_album` → `AlbumInfo` → `download_info_file` / `download_album_images` / `download_tracks`.

- **Album metadata** (`AlbumInfo`): first tries the album's `.txt` info file (`a i.txt_info_file`), parsing `Name:` / `Year:` lines; falls back to the page's `h2` and the `Year:` text node. A name of `Ooops!` means the album page is unavailable and raises `ValueError`.
- **Tracks** are a two-level scrape: album page rows `table#songlist td.playlistDownloadSong a` link to a per-track page, and that page's `a span.songDownloadLink` anchors hold the actual file URLs (one per format). Format filtering is done by matching the file URL's extension.
- **Skip-before-fetch**: for a single format, `get_expected_filename` predicts the local filename from the album-page href so the track page isn't fetched if the file already exists. Album-page hrefs are **double URL-encoded** (`%2520`), hence the double `unquote`. With `--format all` this pre-check is skipped and only the existence check inside `download_file` applies.
- `download_file` derives the filename from `Content-Disposition` or the URL, and skips existing files.

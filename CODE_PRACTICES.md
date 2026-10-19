# Code Practices

Conventions for working on this repository. They describe how the existing code is written; follow them so changes blend in.

## Code style

- Keep everything in `main.py` unless the script grows enough to justify a split. Plain functions, plus a class only when there is state to hold (`AlbumInfo`).
- `snake_case` for functions and variables, `UPPER_CASE` for module-level constants (`BASE_URL`, `DOWNLOAD_DELAY`), declared at the top of the file.
- f-strings for formatting, 4-space indentation, LF line endings.
- Short docstrings only on small helpers whose purpose isn't obvious from the name; comments explain *why* (e.g. the double URL-encoding), not *what*.
- Parse HTML with BeautifulSoup CSS selectors (`soup.select` / `select_one`). Keep selectors close to where they're used.

## HTTP

- Every request goes through the shared `session` (`curl_cffi`, `impersonate="chrome"`). Never call `requests.get` directly or add hand-written browser headers.
- Close streamed responses in a `finally` block.
- Check whether a file already exists *before* making a request whenever the filename can be predicted, to avoid useless traffic.

## Error handling and output

- One failing item (image, track, info file) must not abort the whole album: catch the exception around that item, `print` an error naming the URL, and continue.
- Only `__main__` turns an exception into a fatal error (`An error occurred: ...` + `sys.exit(1)`); `KeyboardInterrupt` exits cleanly.
- User feedback is plain `print` / `sys.stdout.write` (no logging framework). Progress lines rewrite themselves with `\r`.

## Dependencies

- Keep `requirements.txt` minimal and in sync with the imports in `main.py`.
- Use the project venv (`.venv/Scripts/python`) to run and install.

## Testing changes

- There is no test suite. Verify changes by running the script against a real album from a temporary directory (downloads are written to the current directory), and check that the output files are real media (e.g. MP3s start with `ID3`) rather than HTML error pages.
- Delete the temporary download directory afterwards.

## Docs

- When behavior or CLI options change, update `README.md` (user-facing) and `CLAUDE.md` (architecture notes) in the same change.

## Git

- Small commits, one feature or concern per commit (e.g. code fix, README update, and tooling docs are separate commits).
- Commit subject: short imperative sentence in plain English, capitalized, no trailing period (e.g. `Add arg to choose the file type to download`). Add a body when the *why* isn't obvious from the subject.

# GockGet 💅
A multi-threaded XNXX bulk downloader for Python

![CI](https://github.com/bridgette-ryan/gockget/actions/workflows/ci.yml/badge.svg)
![PyPI](https://img.shields.io/pypi/v/gockget)
![Python](https://img.shields.io/pypi/pyversions/gockget)
[![codecov](https://codecov.io/gh/bridgette-ryan/gockget/branch/main/graph/badge.svg)](https://codecov.io/gh/bridgette-ryan/gockget)
![Lint](https://img.shields.io/badge/lint-ruff-purple)
![License](https://img.shields.io/badge/license-GPLv3-blue.svg)

## Welcome Gorgeous 💅

So you found this repo.

Maybe you're here because you needed a practical **XNXX bulk downloader**.

Maybe you're here because some abandoned script from years ago finally collapsed under the weight of neglect.

Maybe you're here because downloading one file at a time is for people with limitless patience and weak convictions.

Maybe you're here because authoritarian governments want to expose your PII to weird and untested third party age verification vendors.

Whatever brought you here:

Welcome, queen.

---

## What Is This?

This is a threaded Python downloader for **XNXX** that reads URLs from `scrape.txt`, downloads multiple videos at once, tracks progress, survives interruptions, and remembers what it was doing when life got messy.

It is efficient, resilient, and only slightly dramatic.

---

## Features

✨ Multi-threaded downloads
✨ Reads URLs from `scrape.txt`
✨ Duplicate filtering
✨ Skips completed items automatically
✨ Retry failed downloads
✨ Detects interrupted partial downloads
✨ Verify mode to repair statuses against disk
✨ Error reset mode
✨ Safe cross-platform filenames
✨ Progress saved automatically
✨ Decorative startup banner with unnecessary glamour
✨ Tested with strong coverage because standards matter

---

## Requirements

You'll need:

* Python 3.11+
* Internet access
* Basic coping skills
* Mild contempt for bad software

## Install

From PyPI (recommended):

```bash
pip install gockget
```

From source:
```bash
git clone https://github.com/bridgette-ryan/gockget.git
cd gockget
pip install .
```

For Development:

```bash
pip install -e .[dev]
```

---

## Optional: Virtual Environment

Because boundaries matter.

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
```

### Windows (Command Prompt)

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
pip install -e .[dev]
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

When you're done:

```bash
deactivate
```

---

## Usage

Run it:

```bash
gockget
```

That will process pending entries in `scrape.txt`.

---

## Command Line Options

### Skip the banner

For days when joy is unavailable.

```bash
gockget --transphobia
```

### Choose thread count

```bash
gockget --threads=8
```

### Retry failed items

```bash
gockget --retry-errors
```

Because healing is possible.

### Reset all errors

```bash
gockget --clear-errors
```

Turns every `ERROR` back into `FALSE`.

### Verify existing files

```bash
gockget --verify
```

Checks files on disk and updates statuses accordingly.

Useful after crashes, interruptions, moving files, or poor decisions.

### Help

```bash
gockget --help
```

---

## scrape.txt Format

```text
URL | SCRAPED | TITLE
https://www.xnxx.com/video-abc123 | FALSE |
https://www.xnxx.com/video-def456 | TRUE | Already_Downloaded
https://www.xnxx.com/video-ghi789 | ERROR | Disaster
```

### Status Meanings

* `FALSE` = never downloaded
* `TRUE` = completed successfully
* `ERROR` = failed attempt
* `PARTIAL` = interrupted download that may be recoverable

Growth is not linear.

---

## File Handling

Downloads are saved using sanitized filenames designed to behave on:

* Windows
* Linux
* macOS

Because no one deserves filename drama.

---

## Recovery

If a download is interrupted, this tool can detect partial states, retry failed items, and verify what actually exists on disk.

We believe in resilience.

---

## Testing

Because confidence is sexy.

```bash
pytest
```

With coverage:

```bash
pytest --cov=app
```

Lint:

```bash
ruff check .
```

This project maintains high automated test coverage.

---

## Project Structure

```text
app/                     core logic
tests/                   unit tests
.github/workflows/       CI pipeline
pyproject.toml           package config
scraped/                 completed downloads
scraping/                temporary files
scrape.txt               input list
```

---

## Notes for the Dolls

If something breaks:

1. Read the traceback.
2. Stay calm.
3. Blame capitalism.
4. Fix it properly.

---

## Contributing

Pull requests welcome.

Especially if you:

* improve performance
* improve reliability
* improve code quality
* improve aesthetics
* bring hot girl engineering energy

---

## Credits

Built using [EchterAlsFake's `xnxx_api`](https://github.com/EchterAlsFake/xnxx_api), which handles the underlying site interaction and download mechanics.

Startup banner image / terminal art inspired by and credited to **Cherry Mavrik**.

This project stands/steps on the cock of glamorous giants.

## Ethical Generative AI Disclosure

AI tools were used to assist with portions of development, including documentation, testing support, and iterative problem solving.

No generated output was accepted blindly. All code was reviewed, tested, modified where necessary, and remains the responsibility of the author.

Human accountability is not optional.

## Disclaimer

Use responsibly.

You are responsible for your use of this software, the content you access, and compliance with local laws, platform rules, and common sense.

Do not be weird about it.

---

## Final Words

This tool is powered by Python, threading, persistence, and feminine spite.

Use it wisely.
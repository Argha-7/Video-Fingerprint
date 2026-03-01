# Video Fingerprint Modification Tool

A robust tool to modify the digital fingerprint of videos by transforming the audio stream and re-encoding without quality loss.

## Features

- **Fingerprint Modification**: Uses FFmpeg `atempo` filter to change audio characteristics and unique signatures.
- **YouTube Support**: Integrated with `yt-dlp` for seamless downloading.
- **GitHub Actions Ready**: Automated workflow for cloud processing.
- **Blogger Integration**: Premium Blogger XML theme for a "one-click" web interface.

## Local Setup

1. Install FFmpeg and add it to your PATH.
2. Install Python dependencies:

   ```bash
   pip install yt-dlp
   ```

3. Run the script:

   ```bash
   python modify_fingerprint.py
   ```

## GitHub Actions & Blogger

Refer to the [setup_guide.md](setup_guide.md) for instructions on how to set up the automated Blogger-to-GitHub pipeline.

#!/bin/bash
# Setup script for the "Gaya CMO – media" cloud environment.
# Installs the tools the CMO agent needs to make visuals: ffmpeg (video and screenshots),
# Montserrat (brand font), Playwright + Chromium (HTML designs to PNG) and faster-whisper (captions).
set -e
SUDO=""
if command -v sudo >/dev/null 2>&1; then SUDO="sudo"; fi
$SUDO apt-get update -y
$SUDO apt-get install -y ffmpeg fonts-montserrat fontconfig
fc-cache -f >/dev/null 2>&1 || true
python3 -m pip install --quiet --upgrade pip
python3 -m pip install --quiet playwright faster-whisper
python3 -m playwright install --with-deps chromium
echo "Gaya CMO media environment ready"

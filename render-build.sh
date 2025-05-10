#!/usr/bin/env bash

# Create chrome dir
mkdir -p .chrome

# Download and extract Chromium
wget https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1181205/chrome-linux.zip
unzip chrome-linux.zip -d .chrome
mv .chrome/chrome-linux .chrome/chromium

# Make chromium executable
chmod +x .chrome/chromium/chrome

# Install pip dependencies
pip install --upgrade pip
pip install -r requirements.txt

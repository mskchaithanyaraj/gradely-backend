#!/usr/bin/env bash

# Create necessary directories
mkdir -p .chrome
mkdir -p .chromedriver

# Download Chromium version 117
wget https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1181205/chrome-linux.zip
unzip chrome-linux.zip -d .chrome
mv .chrome/chrome-linux .chrome/chromium
chmod +x .chrome/chromium/chrome

# Download ChromeDriver v117
wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/117.0.5938.0/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip -d .chromedriver
mv .chromedriver/chromedriver-linux64/chromedriver .chromedriver/chromedriver
chmod +x .chromedriver/chromedriver

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

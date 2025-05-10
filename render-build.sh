#!/bin/bash
# Install dependencies listed in requirements.txt
pip install --upgrade pip
pip install -r requirements.txt  # Ensure this includes selenium and undetected-chromedriver
#!/usr/bin/env bash
apt-get update
apt-get install -y wget gnupg2 unzip
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y ./google-chrome-stable_current_amd64.deb

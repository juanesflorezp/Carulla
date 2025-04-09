#!/usr/bin/env bash

set -e

# Instalar dependencias base
apt-get update
apt-get install -y wget gnupg2 curl unzip

# Instalar Google Chrome estable
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install -y google-chrome-stable

# Verificación
echo "✅ Google Chrome:"
google-chrome --version
which google-chrome

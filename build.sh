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

# Obtener versión exacta de Chrome instalada
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+\.\d+')

# Obtener la última versión compatible de ChromeDriver para esa versión
CHROMEDRIVER_BASE_URL="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing"
CHROMEDRIVER_ZIP_URL=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" \
  | grep -A 10 "\"$CHROME_VERSION\"" \
  | grep -oP 'https://.*?chromedriver-linux64.zip' \
  | head -1)

# Descargar y mover el ChromeDriver
echo "➡️ Descargando ChromeDriver desde $CHROMEDRIVER_ZIP_URL"
curl -Lo chromedriver.zip "$CHROMEDRIVER_ZIP_URL"
unzip chromedriver.zip
mv chromedriver-linux64/chromedriver /usr/bin/chromedriver
chmod +x /usr/bin/chromedriver
rm -rf chromedriver.zip chromedriver-linux64

# Verificaciones
echo "✅ Google Chrome:"
google-chrome --version
echo "✅ ChromeDriver:"
/usr/bin/chromedriver --version

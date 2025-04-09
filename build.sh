#!/usr/bin/env bash

set -e

apt-get update
apt-get install -y wget gnupg2 curl unzip

# Instalar Google Chrome estable
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install -y google-chrome-stable

# Verificar Chrome
which google-chrome-stable
google-chrome-stable --version
ln -sf /usr/bin/google-chrome-stable /usr/bin/google-chrome

# Instalar ChromeDriver compatible
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+' | head -1)
CHROMEDRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" \
    | grep -A 10 "\"$CHROME_VERSION\"" \
    | grep "linux64" \
    | grep -oP 'https://.*?chromedriver-linux64.zip' \
    | head -1)

curl -Lo chromedriver.zip "$CHROMEDRIVER_VERSION"
unzip chromedriver.zip
mv chromedriver-linux64/chromedriver /usr/bin/chromedriver
chmod +x /usr/bin/chromedriver
rm -rf chromedriver.zip chromedriver-linux64

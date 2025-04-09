#!/usr/bin/env bash

apt-get update
apt-get install -y curl unzip gnupg

# Agregar repositorio oficial de Google Chrome
curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Instalar Google Chrome estable
apt-get update
apt-get install -y google-chrome-stable

# Hacer alias para asegurarse de que esté disponible en /usr/bin/google-chrome
ln -s /usr/bin/google-chrome-stable /usr/bin/google-chrome


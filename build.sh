#!/usr/bin/env bash

set -e

apt-get update
apt-get install -y wget gnupg2 curl unzip

# Agregar la clave pública y repositorio oficial de Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Instalar Chrome estable
apt-get update
apt-get install -y google-chrome-stable

# Verificar instalación
which google-chrome-stable
google-chrome-stable --version

# Hacer alias si no existe el binario esperado
ln -sf /usr/bin/google-chrome-stable /usr/bin/google-chrome

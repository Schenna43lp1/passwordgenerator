#!/bin/bash
set -e

##############################################
# Docker Install Script – ONLY Debian 11/12/13
# Author: Markus Stuefer (Optiserve)
##############################################

echo "===== 🐳 Docker Installation gestartet ====="

# --- 0. Prüfen, ob Debian ist ---
if ! grep -qi "debian" /etc/os-release; then
    echo "❌ Fehler: Dieses Script funktioniert NUR auf Debian!"
    echo "Abbruch."
    exit 1
fi

# Debian Version extrahieren
DEBIAN_VERSION=$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2)

if [[ "$DEBIAN_VERSION" != "11" && "$DEBIAN_VERSION" != "12" && "$DEBIAN_VERSION" != "13" ]]; then
    echo "❌ Fehler: Nur Debian 11, 12 und 13 werden unterstützt! Aktuelle Version: $DEBIAN_VERSION"
    exit 1
fi

echo "✔ Debian $DEBIAN_VERSION erkannt – Installation wird fortgesetzt."

# --- 1. Alte Versionen entfernen ---
echo "[1/6] Entferne alte Docker-Versionen..."
sudo apt remove -y docker docker-engine docker.io containerd runc || true

# --- 2. System aktualisieren ---
echo "[2/6] System aktualisieren..."
sudo apt update -y

# --- 3. Benötigte Pakete installieren ---
echo "[3/6] Installiere benötigte Abhängigkeiten..."
sudo apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# --- 4. Docker Repo hinzufügen ---
echo "[4/6] Lade Docker GPG-Key..."
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg \
    | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo "[4/6] Füge Docker Repository hinzu..."
echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# --- 5. Docker installieren ---
echo "[5/6] Installiere Docker Engine + Compose..."
sudo apt update -y
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# --- 6. Docker aktivieren ---
echo "[6/6] Aktiviere Docker Dienst..."
sudo systemctl enable docker
sudo systemctl start docker

echo "===== ✅ Docker Installation abgeschlossen ====="
docker --version
docker compose version

#!/bin/bash

# Pet Talk Automation - Kurulum Scripti

echo "🚀 Pet Talk Automation Kurulumu Başlatılıyor..."

# Git pull
echo "📥 Son değişiklikler alınıyor..."
git pull origin main

# Pillow versiyonunu düzelt
echo "🔧 requirements.txt düzeltiliyor..."
sed -i 's/Pillow==11.1.0/Pillow==10.1.0/' requirements.txt

# Venv oluştur veya etkinleştir
if [ ! -d ".venv" ]; then
    echo "🐍 Sanal ortam oluşturuluyor..."
    python3 -m venv .venv
fi

source .venv/bin/activate

# Paketleri yükle
echo "📦 Paketler yükleniyor..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# .env dosyasını oluştur (yoksa)
if [ ! -f ".env" ]; then
    echo "⚙️ .env dosyası oluşturuluyor..."
    cp .env.example .env
    echo "⚠️ UYARI: .env dosyasını API anahtarlarınızla doldurun!"
fi

# Dizinleri oluştur
mkdir -p videos/output
mkdir -p data

echo "✅ Kurulum tamamlandı!"
echo "🎬 Videoyu başlatmak için şunu çalıştırın: python -m src.main"

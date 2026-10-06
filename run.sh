#!/bin/bash

# Pet Talk Automation - Başlatma Scripti

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Sanal ortamı etkinleştir
if [ ! -d ".venv" ]; then
    echo "⚠️ Sanal ortam bulunamadı! Kurulum yapılıyor..."
    bash setup.sh
fi

source .venv/bin/activate

# .env kontrolü
if [ ! -f ".env" ]; then
    echo "⚠️ .env dosyası bulunamadı! .env.example kopyalanıyor..."
    cp .env.example .env
    echo "⚠️ UYARI: .env dosyasını doldurmalısınız!"
    echo "   - ANTHROPIC_API_KEY: Claude API anahtarı"
    echo "   - ELEVENLABS_API_KEY: ElevenLabs API anahtarı"
    echo "   - YOUTUBE_CLIENT_ID ve SECRET: YouTube OAuth bilgileri"
    exit 1
fi

# Dizinleri kontrol et
mkdir -p videos/output
mkdir -p data

echo ""
echo "╔════════════════════════════════════════╗"
echo "║     🎬 Pet Talk Automation System      ║"
echo "║           $(date +%Y-%m-%d' '%H:%M:%S)           ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Video oluştur ve yükle
echo "🎥 Video oluşturuluyor..."
python -m src.main

# Video dosyasını bul
LATEST_VIDEO=$(ls -t videos/output/*.mp4 2>/dev/null | head -1)

if [ -n "$LATEST_VIDEO" ]; then
    echo ""
    echo "✅ Video başarıyla oluşturuldu!"
    echo "📁 Konum: $LATEST_VIDEO"
    echo "📊 Boyut: $(du -h "$LATEST_VIDEO" | cut -f1)"
    echo ""
    echo "🎉 Sistem başarıyla tamamlandı!"
else
    echo "❌ Video bulunamadı!"
    exit 1
fi

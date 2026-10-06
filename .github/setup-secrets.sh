#!/bin/bash

# GitHub Actions Secrets Kurulumu Hızlandırıcı
# Bu script size secrets eklemenize yardımcı olur

echo "🔐 GitHub Actions Secrets Kurulumu"
echo "=================================="
echo ""

# Gereken secrets listesi
secrets=(
    "ANTHROPIC_API_KEY"
    "ELEVENLABS_API_KEY"
    "ELEVENLABS_VOICE_ID_CAT"
    "ELEVENLABS_VOICE_ID_DOG"
    "YOUTUBE_CLIENT_ID"
    "YOUTUBE_CLIENT_SECRET"
    "YOUTUBE_CHANNEL_ID"
)

echo "Aşağıdaki secrets'i GitHub'a eklemeniz gerekiyor:"
echo ""

for secret in "${secrets[@]}"; do
    echo "📌 $secret"
    echo "   Repository → Settings → Secrets and variables → Actions → New repository secret"
    echo "   Name: $secret"
    echo "   Value: [değeri gir]"
    echo ""
done

echo "✅ Tüm secrets eklendikten sonra workflow otomatik olarak çalışacak!"
echo ""
echo "📅 Zamanlama: Her gün 09:00 UTC"
echo "🎥 Sonuçlar: Actions sekmesinde artifacts'te"

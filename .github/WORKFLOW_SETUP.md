# Pet Talk Automation GitHub Actions Kurulu

GitHub Actions otomasyonu şu işleri otomatik yapacak:

## 📅 Zamanlama
- **Her gün saat 09:00 UTC'de** otomatik çalışır
- Manuel olarak da tetiklenebilir (workflow_dispatch)

## 🔄 İş Akışı

1. **Repository'yi indir** → En son kodu buluttan çeker
2. **Python 3.12 yükle** → Uyumlu ortam hazırlar
3. **Bağımlılıkları yükle** → Tüm paketleri kurar
4. **.env dosyasını oluştur** → GitHub Secrets'ten API anahtarlarını kullanır
5. **Klasörleri oluştur** → videos/output ve data dizinleri
6. **Video üret** → `python -m src.main` çalıştırır
7. **Artifacts'e yükle** → Videoyu GitHub'a kaydeder
8. **İstatistik gönder** → Rapor oluşturur

## 🔐 Gereken GitHub Secrets

`.github/workflows/daily-video.yml` dosyasında bu secretlar kullanılıyor:

```
ANTHROPIC_API_KEY          → Claude API anahtarı
ELEVENLABS_API_KEY         → ElevenLabs sesler
ELEVENLABS_VOICE_ID_CAT    → Kedi sesi ID'si
ELEVENLABS_VOICE_ID_DOG    → Köpek sesi ID'si
YOUTUBE_CLIENT_ID          → YouTube OAuth ID
YOUTUBE_CLIENT_SECRET      → YouTube OAuth Secret
YOUTUBE_CHANNEL_ID         → Hangi kanala yükleneceği
```

## ⚙️ Kurulum

### 1. Secrets'i GitHub'a ekle

Repository Settings → Secrets and variables → Actions

Her biri için yeni secret ekle:
- Name: `ANTHROPIC_API_KEY`
- Value: `sk-ant-...` (gerçek anahtarın)

Aynı şekilde diğer tüm secrets'i ekle.

### 2. Workflow'u kontrol et

Actions sekmesinde `daily-video.yml` görülmeli.

### 3. Manuel olarak çalıştır

Actions → Select workflow → Run workflow

## 📊 Sonuçlar

Her çalıştırma sonrası:
- Video: `Artifacts` sekmesinde indirilir
- Veritabanı: 30 gün saklanır
- Log: Workflow çalıştırma detaylarında görülür

## 🎯 Avantajlar

✅ Terminal açmaya gerek yok
✅ Her gün otomatik çalışır
✅ Başarısız olursa GitHub bildirir
✅ Videoları GitHub tarafında saklar
✅ Tam otomasyonlu sistem

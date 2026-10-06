# Pet Talk Automation

Kedi ve köpek karakterleri için her gün otomatik senaryo üreten, AI seslendirme ile konuşan ve YouTube'a yükleyen tam otomasyon sistemi.

## Özellikler

- Kedi ve köpek için ayrı karakter profilleri
- Günlük otomatik senaryo üretimi
- 20 saniyelik video üretimi
- Seslendirme için ElevenLabs desteği
- YouTube yükleme akışı
- SQLite ile takibi
- GitHub Actions ile otomatik çalıştırma
- Docker ve Python desteği

## Özelleştirilebilir senaryo yapısı

- Kedi: kibirli, akıllı, alaycı
- Köpek: enerjik, dost canlısı, coşkulu
- Konuşmalar güncel gündelik olaylara göre üretilebilir
- Her gün farklı başlık, sahne ve ton

## Klasör yapısı

```text
pet-talk-automation/
├── .github/
│   └── workflows/
│       └── daily-upload.yml
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── character_profiles.py
│   ├── scenario_generator.py
│   ├── voice_generator.py
│   ├── video_creator.py
│   ├── database.py
│   ├── youtube_uploader.py
│   └── main.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── videos/
```

## Kurulum

```bash
git clone https://github.com/yalmaz665-dotcom/pet-talk-automation.git
cd pet-talk-automation
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m src.main
```

## Çevre değişkenleri

Aşağıdaki değerleri `.env` içine yazın:

```env
ANTHROPIC_API_KEY=
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE_ID_CAT=
ELEVENLABS_VOICE_ID_DOG=
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
YOUTUBE_REDIRECT_URI=http://localhost:8080/oauth2callback
YOUTUBE_CHANNEL_ID=
OUTPUT_DIR=./videos/output
DATABASE_PATH=./data/videos.db
VIDEO_DURATION=20
VIDEO_FPS=30
VIDEO_WIDTH=1920
VIDEO_HEIGHT=1080
LOG_LEVEL=INFO
DEFAULT_LANGUAGE=tr
```

## Senaryo örneği

```json
{
  "title": "Kedi ve Köpek Kahvaltı Savaşı",
  "theme": "komedi",
  "duration": 20,
  "date": "2026-10-06",
  "scenes": [
    {"speaker": "cat", "text": "Bu kahvaltı masasında ben başrolüm!", "duration": 5, "emotion": "gururlu", "action": "walk"},
    {"speaker": "dog", "text": "Nooo! Benim enerjim daha çok!", "duration": 5, "emotion": "coşkulu", "action": "tail_wag"},
    {"speaker": "cat", "text": "Sen gülünç bir köpektin, ama ben çok zarifim.", "duration": 5, "emotion": "alaycı", "action": "pounce"},
    {"speaker": "dog", "text": "Şimdi ben seni yeneceğim, hadi oyun zamanı!", "duration": 5, "emotion": "kararlı", "action": "run"}
  ],
  "script": [
    "Mavi: Bu kahvaltı masasında ben başrolüm!",
    "Bozkurt: Nooo! Benim enerjim daha çok!",
    "Mavi: Sen gülünç bir köpektin, ama ben çok zarifim.",
    "Bozkurt: Şimdi ben seni yeneceğim, hadi oyun zamanı!"
  ],
  "background_music": "light_funny"
}
```

## YouTube yükleme

```bash
python -m src.youtube_uploader --video ./videos/output/2026-10-06_pet_talk.mp4 --title "Kedi ve Köpek Kahvaltı Savaşı"
```

## Günlük otomatik çalıştırma

GitHub Actions akışı her gün saat 09:00 UTC'de çalışır.

## Notlar

- API anahtarları `.env` içinde tutulur.
- `FFmpeg` sisteminizde kurulu olmalıdır.
- İlk YouTube yüklemede OAuth ekranı açılacaktır.
- Eğer API anahtarı yoksa sistem otomatik olarak yerel fallback senaryo üretir.

---

Yapılandırılmış ve genişletilebilir bir başlangıç depodur. İsterseniz bunu bir sonraki adımda tam üretim kodu ve karakter hareketleriyle daha gelişmiş hale getirebiliriz.

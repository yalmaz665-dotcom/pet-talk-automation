import json
import logging
from datetime import datetime
from typing import Dict, List, Any

from anthropic import Anthropic

from src.character_profiles import build_character_map
from src.config import config

logging.basicConfig(level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

DAILY_SCENARIOS = [
    {
        "theme": "kahvaltı",
        "topics": ["balık", "ekmek", "süt", "yumurta"],
        "conflict": "Kim daha önce yeme hakkı var?"
    },
    {
        "theme": "oyun",
        "topics": ["top", "ip", "pençe", "kuyruğu tutma"],
        "conflict": "Nasıl oynanacağı konusunda anlaşamazlar"
    },
    {
        "theme": "uyku",
        "topics": ["yatak", "yastık", "ışık", "sessizlik"],
        "conflict": "Kedi uyku isteriyor, köpek oyun istiyor"
    },
    {
        "theme": "temizlik",
        "topics": ["banyo", "tırnak", "yüz", "pençe"],
        "conflict": "Kedi temiz, köpek kirli"
    },
    {
        "theme": "macera",
        "topics": ["bahçe", "bahçe kapısı", "komşu hayvanı", "kuş"],
        "conflict": "Farklı hedefleri var"
    },
    {
        "theme": "yemek seçimi",
        "topics": ["balıklı mama", "etli mama", "kuru mama"],
        "conflict": "Hangisi daha leziz?"
    },
    {
        "theme": "yer seçimi",
        "topics": ["pencere kenarı", "kanapé", "halı", "güneş"],
        "conflict": "Tek bir yer var, ikisi de istiyor"
    },
    {
        "theme": "ziyaretçi",
        "topics": ["çan çalma", "kapı", "tanışma", "selamlaşma"],
        "conflict": "Farklı selamlaşma stilleri"
    }
]

def _build_scenario_prompt(theme_data: Dict[str, Any]) -> str:
    cat = build_character_map()["cat"]
    dog = build_character_map()["dog"]
    
    return f"""
Türkçe olarak 20 saniyelik komik bir video senaryosu yaz.

TEMA: {theme_data['theme']}
KONULAR: {', '.join(theme_data['topics'])}
ÇATIŞMA: {theme_data['conflict']}

KARİ PROFILLER:
KÖPEĞİ (Bozkurt): {dog.personality}
- Ses Tonu: {dog.voice_tone}
- Konuşma Stili: {dog.speaking_style}

KEDİ (Mavi): {cat.personality}
- Ses Tonu: {cat.voice_tone}
- Konuşma Stili: {cat.speaking_style}

KURALLAR:
1. Tam 4 sahne olsun
2. Her sahne 5 saniye olsun (toplam 20 saniye)
3. Kedi ve köpek arası diyalog olsun
4. İlk sahne: Kedi açılış yapıyor (kibirli/alayci)
5. İkinci sahne: Köpek cevap veriyor (coşkulu/neşeli)
6. Üçüncü sahne: Kedi bir yorum yapıyor (alaycı/akıllı)
7. Dördüncü sahne: Köpek harekete geçiyor (enerjik/kararlı)
8. Her karakter 1-2 cümle konuşsun
9. Cümleler kısa ve komik olsun
10. Konuşmalar doğal ve eğlenceli olsun

JSON FORMAT (sadece JSON döndür, başka bir şey yazma):
{{
  "title": "Başlık buraya",
  "theme": "{theme_data['theme']}",
  "duration": 20,
  "date": "{datetime.utcnow().strftime('%Y-%m-%d')}",
  "scenes": [
    {{"speaker": "cat", "text": "Metin buraya", "duration": 5, "emotion": "gururlu", "action": "walk"}},
    {{"speaker": "dog", "text": "Metin buraya", "duration": 5, "emotion": "coşkulu", "action": "tail_wag"}},
    {{"speaker": "cat", "text": "Metin buraya", "duration": 5, "emotion": "alaycı", "action": "pounce"}},
    {{"speaker": "dog", "text": "Metin buraya", "duration": 5, "emotion": "kararlı", "action": "run"}}
  ]
}}

Başarıyla yap! Komik, net ve profesyonel olsun.
"""

def generate_daily_scenario(date_str: str = None) -> Dict[str, Any]:
    """Her gün için yeni senaryo üret"""
    if not date_str:
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
    
    if not config.ANTHROPIC_API_KEY:
        logger.warning("ANTHROPIC_API_KEY bulunamadı. Fallback senaryo üretiliyor.")
        return _fallback_scenario(date_str)
    
    try:
        import random
        theme_data = random.choice(DAILY_SCENARIOS)
        prompt = _build_scenario_prompt(theme_data)
        
        client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text
        
        # JSON'ı extract et
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            scenario = json.loads(json_str)
            scenario["date"] = date_str
            logger.info(f"Senaryo başarıyla üretildi: {scenario['title']}")
            return scenario
        else:
            logger.error("JSON bulunamadı. Fallback kullanılıyor.")
            return _fallback_scenario(date_str)
            
    except Exception as e:
        logger.error(f"Senaryo üretimi hatası: {e}. Fallback kullanılıyor.")
        return _fallback_scenario(date_str)

def _fallback_scenario(date_str: str) -> Dict[str, Any]:
    """Yedek senaryo"""
    return {
        "title": "Kedi vs Köpek: Kahvaltı Savaşı",
        "theme": "kahvaltı",
        "duration": 20,
        "date": date_str,
        "scenes": [
            {
                "speaker": "cat",
                "text": "Bu sabah balığı ben yiyorum! Benim seçkin tadım var!",
                "duration": 5,
                "emotion": "gururlu",
                "action": "walk"
            },
            {
                "speaker": "dog",
                "text": "Hayır! Ben daha çok ihtiyaç duyduk! Hadi paylaşalım!",
                "duration": 5,
                "emotion": "coşkulu",
                "action": "tail_wag"
            },
            {
                "speaker": "cat",
                "text": "Sen sadece acıkıyorsun, ben gourmet'im. Fark anla!",
                "duration": 5,
                "emotion": "alaycı",
                "action": "pounce"
            },
            {
                "speaker": "dog",
                "text": "Tamam! O zaman ben seni kovalamaya başlıyorum!",
                "duration": 5,
                "emotion": "kararlı",
                "action": "run"
            }
        ]
    }

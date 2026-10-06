from dataclasses import dataclass
from typing import List

@dataclass
class CharacterProfile:
    """Karakter profili tanımı"""
    name: str
    species: str
    personality: str
    voice_tone: str
    speaking_style: str
    favorite_topics: List[str]
    emotion_mapping: dict

def get_cat_profile() -> CharacterProfile:
    """Kedi karakter profili - Mavi"""
    return CharacterProfile(
        name="Mavi",
        species="cat",
        personality="Akıllı, kibirli, alaycı, bağımsız, zarif",
        voice_tone="İnce, zarif, hafif alaycı, üstünlük duygusu",
        speaking_style="Kısa keskin cümleler, dalga geçer, tepeden bakar",
        favorite_topics=["balık", "gün ışığı", "bağımsızlık", "uyku", "temizlik", "estetik"],
        emotion_mapping={
            "gururlu": "Benim seçkin tarafımı göster",
            "alaycı": "Köpeği küçültme, kendini üstün göster",
            "öfkeli": "Hırlamayı taklit et, tehdit et",
            "sakin": "Rahat ve üstünlük duygusu",
            "oyuncu": "Dahice bir oyun oynuyorum"
        }
    )

def get_dog_profile() -> CharacterProfile:
    """Köpek karakter profili - Bozkurt"""
    return CharacterProfile(
        name="Bozkurt",
        species="dog",
        personality="Enerjik, dost canlısı, coşkulu, sadık, hareketli",
        voice_tone="Gür, sıcak, neşeli, enerjik, heyecanlı",
        speaking_style="Hızlı konuşma, coşku dolu, pozitif enerji, tekrar eden sözcükler",
        favorite_topics=["oyun", "kahvaltı", "koşu", "arkadaşlık", "macera", "eğlence"],
        emotion_mapping={
            "coşkulu": "Çok heyecanlı, yüksek enerji",
            "mutlu": "Neşeli ve dost canlı",
            "kararlı": "Mücadele etmeye hazır",
            "meraklı": "Yeni şeyler keşfetmek istiyor",
            "şaşkın": "Kediyi anlamıyor"
        }
    )

def build_character_map() -> dict:
    """Tüm karakterleri harita halinde döndür"""
    return {
        "cat": get_cat_profile(),
        "dog": get_dog_profile()
    }

def get_character(species: str) -> CharacterProfile:
    """Karakter getir"""
    characters = build_character_map()
    return characters.get(species)

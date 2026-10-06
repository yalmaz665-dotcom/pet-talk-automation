import logging
import os
from pathlib import Path
from typing import Optional

from elevenlabs import generate, save, set_api_key

from src.config import config

logging.basicConfig(level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

def generate_character_audio(text: str, speaker: str, output_path: str) -> str:
    """
    Karakter için ses oluştur (ElevenLabs kullanarak)
    speaker: "cat" veya "dog"
    """
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not config.ELEVENLABS_API_KEY:
        logger.warning(f"ElevenLabs API key yok. {speaker} için dummy ses oluşturuluyor.")
        _create_dummy_audio(output_path, speaker)
        return output_path
    
    try:
        set_api_key(config.ELEVENLABS_API_KEY)
        
        # Karakter seçimi
        if speaker == "cat":
            voice_id = config.ELEVENLABS_VOICE_ID_CAT
            stability = 0.6  # Daha değişken
            similarity_boost = 0.75
        else:  # dog
            voice_id = config.ELEVENLABS_VOICE_ID_DOG
            stability = 0.7
            similarity_boost = 0.8
        
        if not voice_id:
            logger.warning(f"Voice ID {speaker} için tanımlanmamış. Dummy ses oluşturuluyor.")
            _create_dummy_audio(output_path, speaker)
            return output_path
        
        # Ses oluştur
        audio = generate(
            text=text,
            voice=voice_id,
            model="eleven_turbo_v2",
            stream=False
        )
        
        # Dosyaya kaydet
        save(audio, output_path)
        logger.info(f"✓ {speaker.upper()} seslendirmesi başarıyla oluşturuldu: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"ElevenLabs hata ({speaker}): {e}. Dummy ses oluşturuluyor.")
        _create_dummy_audio(output_path, speaker)
        return output_path

def _create_dummy_audio(output_path: str, speaker: str) -> None:
    """API yok ise dummy wav dosyası oluştur"""
    try:
        import wave
        import math
        
        sample_rate = 22050
        duration = 3  # 3 saniye
        frequency = 220 if speaker == "cat" else 140  # Kedi yüksek, köpek alçak
        
        num_samples = sample_rate * duration
        frames = []
        
        for i in range(num_samples):
            sample = int(32767 * 0.3 * math.sin(2 * math.pi * frequency * i / sample_rate))
            frames.append(sample)
        
        with wave.open(output_path, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            
            for frame in frames:
                wav_file.writeframes(frame.to_bytes(2, byteorder='little', signed=True))
        
        logger.info(f"✓ Dummy {speaker} sesi oluşturuldu: {output_path}")
        
    except Exception as e:
        logger.error(f"Dummy ses oluşturulamadı: {e}")

def generate_scenario_audio(scenario: dict) -> dict:
    """
    Senaryo için tüm karakterleri seslendir
    """
    output_dir = Path(config.OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    audio_files = {}
    
    for idx, scene in enumerate(scenario.get("scenes", []), 1):
        speaker = scene["speaker"]
        text = scene["text"]
        
        # Dosya adı
        filename = f"{scenario['date']}_{speaker}_{idx}.wav"
        output_path = str(output_dir / filename)
        
        # Ses oluştur
        audio_path = generate_character_audio(text, speaker, output_path)
        audio_files[f"{speaker}_{idx}"] = audio_path
    
    return audio_files

import logging
from pathlib import Path
from typing import Dict, Any

from moviepy.editor import (
    ColorClip, TextClip, CompositeVideoClip, ImageClip, concatenate_videoclips
)
from PIL import Image, ImageDraw, ImageFont

from src.config import config

logging.basicConfig(level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

def _create_character_frame(species: str, emotion: str, size: tuple = (1920, 1080)) -> Image.Image:
    """
    Karakter frame'i oluştur (PIL ile basit görsel)
    species: "cat" veya "dog"
    emotion: "happy", "angry", "proud", "excited" vb.
    """
    # Arka plan rengi
    if species == "cat":
        bg_color = (255, 200, 100)  # Kedi için sıcak sarı
    else:
        bg_color = (135, 206, 235)  # Köpek için mavi
    
    image = Image.new("RGB", size, bg_color)
    draw = ImageDraw.Draw(image)
    
    # Basit karakterler çiz
    center_x, center_y = size[0] // 2, size[1] // 2
    
    if species == "cat":
        # Kedi baş
        draw.ellipse([center_x - 150, center_y - 150, center_x + 150, center_y + 150], 
                     fill=(255, 180, 80), outline=(0, 0, 0), width=3)
        
        # Kulaklar
        draw.polygon([(center_x - 100, center_y - 160), 
                      (center_x - 80, center_y - 250), 
                      (center_x - 60, center_y - 160)], 
                     fill=(255, 160, 60))
        draw.polygon([(center_x + 60, center_y - 160), 
                      (center_x + 80, center_y - 250), 
                      (center_x + 100, center_y - 160)], 
                     fill=(255, 160, 60))
        
        # Gözler
        draw.ellipse([center_x - 60, center_y - 60, center_x - 30, center_y - 20], 
                     fill=(0, 0, 0))
        draw.ellipse([center_x + 30, center_y - 60, center_x + 60, center_y - 20], 
                     fill=(0, 0, 0))
        
        # Burun
        draw.polygon([(center_x, center_y), (center_x - 15, center_y + 20), 
                      (center_x + 15, center_y + 20)], fill=(255, 100, 100))
        
        # Ağız (duyguya göre)
        if emotion in ["happy", "excited"]:
            draw.arc([center_x - 40, center_y, center_x + 40, center_y + 80], 
                     0, 180, fill=(0, 0, 0), width=3)
        elif emotion == "angry":
            draw.line([(center_x - 40, center_y + 30), (center_x + 40, center_y + 30)], 
                      fill=(0, 0, 0), width=3)
        
    else:  # dog
        # Köpek baş
        draw.ellipse([center_x - 120, center_y - 100, center_x + 120, center_y + 140], 
                     fill=(180, 140, 100), outline=(0, 0, 0), width=3)
        
        # Kulaklar
        draw.ellipse([center_x - 140, center_y - 80, center_x - 80, center_y + 40], 
                     fill=(160, 120, 80))
        draw.ellipse([center_x + 80, center_y - 80, center_x + 140, center_y + 40], 
                     fill=(160, 120, 80))
        
        # Gözler
        draw.ellipse([center_x - 60, center_y - 40, center_x - 30, center_y - 10], 
                     fill=(0, 0, 0))
        draw.ellipse([center_x + 30, center_y - 40, center_x + 60, center_y - 10], 
                     fill=(0, 0, 0))
        
        # Burun
        draw.ellipse([center_x - 20, center_y + 20, center_x + 20, center_y + 50], 
                     fill=(50, 50, 50))
        
        # Ağız (duyguya göre)
        if emotion in ["happy", "excited"]:
            draw.line([(center_x - 30, center_y + 50), (center_x - 30, center_y + 80)], 
                      fill=(0, 0, 0), width=3)
            draw.line([(center_x + 30, center_y + 50), (center_x + 30, center_y + 80)], 
                      fill=(0, 0, 0), width=3)
        elif emotion == "angry":
            draw.line([(center_x - 50, center_y + 60), (center_x + 50, center_y + 60)], 
                      fill=(0, 0, 0), width=4)
    
    return image

def create_video_from_scenario(scenario: Dict[str, Any], output_path: str) -> str:
    """
    Senaryo'dan 20 saniyelik video oluştur
    """
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    clips = []
    current_time = 0.0
    
    try:
        for scene in scenario.get("scenes", []):
            speaker = scene["speaker"]
            text = scene["text"]
            duration = float(scene.get("duration", 5))
            emotion = scene.get("emotion", "happy")
            
            # Karakter frame'i oluştur
            char_image = _create_character_frame(speaker, emotion, (config.VIDEO_WIDTH, 800))
            char_path = str(output_dir / f"char_{speaker}_{current_time}.png")
            char_image.save(char_path)
            
            # Karakteri video clip'e çevir
            char_clip = ImageClip(char_path).set_duration(duration)
            
            # Konuşma metni için text clip
            text_clip = TextClip(
                text,
                fontsize=48,
                color="white",
                font="Arial-Bold",
                method="caption",
                size=(config.VIDEO_WIDTH - 100, 200),
                align="center",
                stroke_color="black",
                stroke_width=2
            ).set_duration(duration).set_position(("center", config.VIDEO_HEIGHT - 250))
            
            # Arka plan
            bg_clip = ColorClip(
                size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT),
                color=(30, 30, 50)
            ).set_duration(duration)
            
            # Sahneleri birleştir
            scene_clip = CompositeVideoClip([
                bg_clip,
                char_clip.set_position(("center", "top")),
                text_clip
            ], size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT))
            
            clips.append(scene_clip)
            current_time += duration
        
        # Tüm sahneleri birleştir
        if clips:
            final_video = concatenate_videoclips(clips)
            final_video.write_videofile(
                output_path,
                fps=config.VIDEO_FPS,
                codec="libx264",
                audio_codec="aac",
                verbose=False,
                logger=None
            )
            logger.info(f"✓ Video başarıyla oluşturuldu: {output_path}")
            return output_path
        else:
            logger.error("Clip'ler boş, video oluşturulamadı")
            return ""
    
    except Exception as e:
        logger.error(f"Video oluşturma hatası: {e}")
        return ""

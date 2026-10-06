import logging
from datetime import datetime

from src.config import config
from src.scenario_generator import generate_daily_scenario
from src.voice_generator import generate_scenario_audio
from src.video_creator import create_video_from_scenario
from src.youtube_uploader import upload_video
from src.database import save_video_record

logging.basicConfig(level=config.LOG_LEVEL, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

def main():
    date_text = datetime.utcnow().strftime('%Y-%m-%d')
    logger.info('🎬 Pet automation başlatıldı.')
    
    try:
        scenario = generate_daily_scenario(date_text)
        logger.info(f"✓ Senaryo hazır: {scenario.get('title')}")
        
        audio_map = generate_scenario_audio(scenario)
        logger.info(f"✓ Sesler hazır: {len(audio_map)} dosya")
        
        output_path = f"{config.OUTPUT_DIR}/{date_text}_pet_video.mp4"
        video_path = create_video_from_scenario(scenario, output_path)
        
        if not video_path:
            logger.error('✗ Video oluşturulamadı.')
            return
        
        logger.info(f"✓ Video hazır: {video_path}")
        save_video_record(date_text, scenario.get('title'), video_path, status='created')
        
        result = upload_video(video_path, scenario.get('title'), 'Günlük kedi ve köpek diyaloğu')
        logger.info(f"✓ Upload sonucu: {result}")
        
        save_video_record(date_text, scenario.get('title'), video_path, 
                         status='uploaded' if result.get('status') == 'uploaded' else 'created')
        
        logger.info('🎉 İşlem tamamlandı!')
        
    except Exception as e:
        logger.error(f'✗ Hata: {e}', exc_info=True)

if __name__ == '__main__':
    main()

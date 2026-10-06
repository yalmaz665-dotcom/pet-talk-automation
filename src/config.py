import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Anthropic API
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # ElevenLabs API
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
    ELEVENLABS_VOICE_ID_CAT = os.getenv("ELEVENLABS_VOICE_ID_CAT", "")
    ELEVENLABS_VOICE_ID_DOG = os.getenv("ELEVENLABS_VOICE_ID_DOG", "")
    
    # YouTube OAuth2
    YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "")
    YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
    YOUTUBE_REDIRECT_URI = os.getenv("YOUTUBE_REDIRECT_URI", "http://localhost:8080/oauth2callback")
    YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID", "")
    
    # Video Settings
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./videos/output")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/videos.db")
    VIDEO_DURATION = int(os.getenv("VIDEO_DURATION", "20"))
    VIDEO_FPS = int(os.getenv("VIDEO_FPS", "30"))
    VIDEO_WIDTH = int(os.getenv("VIDEO_WIDTH", "1920"))
    VIDEO_HEIGHT = int(os.getenv("VIDEO_HEIGHT", "1080"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "tr")

config = Config()

"""Configuration file"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    FIREBASE_CREDENTIALS = os.environ.get('FIREBASE_CREDENTIALS', 'firebase/serviceAccountKey.json')
    YOLO_MODEL_PATH = 'weights/yolov8n.pt'
    
    LANGUAGES = {
        'te': 'Telugu', 'hi': 'Hindi', 'en': 'English',
        'es': 'Spanish', 'de': 'German', 'fr': 'French',
        'it': 'Italian', 'ja': 'Japanese', 'ko': 'Korean',
        'zh-cn': 'Chinese (Simplified)'
    }

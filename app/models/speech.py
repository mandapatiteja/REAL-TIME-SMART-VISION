"""
Text-to-Speech Module using gTTS - FIXED VERSION
"""
from gtts import gTTS
import os
import uuid

def generate_speech(text, language='en', slow=False):
    '''
    Generate speech from text using gTTS
    
    Args:
        text: Text to convert to speech
        language: Language code (default: 'en')
        slow: Whether to speak slowly (default: False)
    
    Returns:
        ONLY the filename (not full path)
    '''
    try:
        # Create audio directory if it doesn't exist
        audio_dir = os.path.join('static', 'audio')
        os.makedirs(audio_dir, exist_ok=True)
        
        # Generate unique filename
        filename = f"{uuid.uuid4().hex[:8]}_{language}.mp3"
        filepath = os.path.join(audio_dir, filename)
        
        print(f"[{language}] Generating audio...")
        print(f"[{language}] Text length: {len(text)} chars")
        print(f"[{language}] Saving to: {filepath}")
        
        # Generate speech
        tts = gTTS(text=text, lang=language, slow=slow)
        tts.save(filepath)
        
        # Verify file exists
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"[{language}] ✓ Saved: {filepath} ({size} bytes)")
            print(f"[{language}] ✓ Returning filename: {filename}")
            return filename  # ONLY filename, NOT full path
        else:
            print(f"[{language}] ✗ File not created")
            return None
        
    except Exception as e:
        print(f"[{language}] ✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def generate_multilingual_audio(text_dict, languages):
    '''
    Generate audio files for multiple languages
    
    Args:
        text_dict: Dictionary with language codes as keys and text as values
        languages: List of language codes
    
    Returns:
        Dictionary with language codes and corresponding audio filenames
    '''
    audio_files = {}
    
    for lang in languages:
        if lang in text_dict:
            audio_file = generate_speech(text_dict[lang], language=lang)
            if audio_file:
                audio_files[lang] = audio_file
                print(f"[{lang}] ✓ Audio ready: {audio_file}")
            else:
                print(f"[{lang}] ✗ Audio failed")
    
    return audio_files

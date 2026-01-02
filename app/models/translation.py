"""
Translation Module using Googletrans
"""
from googletrans import Translator

translator = Translator()

def translate_text(text, source_lang='en', target_lang='hi'):
    '''
    Translate text from source language to target language
    
    Args:
        text: Text to translate
        source_lang: Source language code (default: 'en')
        target_lang: Target language code (default: 'hi')
    
    Returns:
        Translated text string
    '''
    try:
        translation = translator.translate(text, src=source_lang, dest=target_lang)
        return translation.text
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return text  # Return original text if translation fails

def detect_language(text):
    '''
    Detect the language of given text
    
    Args:
        text: Input text
    
    Returns:
        Detected language code
    '''
    try:
        detection = translator.detect(text)
        return detection.lang
    except Exception as e:
        print(f"Language detection error: {str(e)}")
        return 'en'  # Default to English

def translate_multiple(text, target_languages):
    '''
    Translate text to multiple languages
    
    Args:
        text: Text to translate
        target_languages: List of target language codes
    
    Returns:
        Dictionary with language codes as keys and translations as values
    '''
    translations = {}
    
    for lang in target_languages:
        try:
            translated = translate_text(text, target_lang=lang)
            translations[lang] = translated
        except Exception as e:
            print(f"Error translating to {lang}: {str(e)}")
            translations[lang] = text
    
    return translations

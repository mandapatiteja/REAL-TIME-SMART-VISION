"""
Celebrity Recognition Module
Uses face recognition + Wikipedia API to identify famous people
"""
import face_recognition
import wikipedia
import requests
from PIL import Image
import numpy as np
import os
import pickle

# Celebrity face database
CELEBRITY_DB_PATH = 'celebrity_faces.pkl'

def load_celebrity_database():
    """Load pre-saved celebrity face encodings"""
    if os.path.exists(CELEBRITY_DB_PATH):
        with open(CELEBRITY_DB_PATH, 'rb') as f:
            return pickle.load(f)
    return {}

def save_celebrity_database(database):
    """Save celebrity face encodings"""
    with open(CELEBRITY_DB_PATH, 'wb') as f:
        pickle.dump(database, f)

def add_celebrity_to_database(name, image_path):
    """
    Add a celebrity to the recognition database
    
    Args:
        name: Celebrity name (e.g., "Elon Musk", "Taylor Swift")
        image_path: Path to celebrity image
    
    Returns:
        Boolean indicating success
    """
    try:
        # Load image
        image = face_recognition.load_image_file(image_path)
        
        # Get face encodings
        encodings = face_recognition.face_encodings(image)
        
        if len(encodings) > 0:
            # Load existing database
            db = load_celebrity_database()
            
            # Add new celebrity
            db[name] = encodings[0]
            
            # Save database
            save_celebrity_database(db)
            
            print(f"✅ Added {name} to celebrity database")
            return True
        else:
            print(f"❌ No face found in image for {name}")
            return False
    
    except Exception as e:
        print(f"Error adding celebrity: {str(e)}")
        return False

def recognize_celebrity(image_path, tolerance=0.6):
    """
    Recognize celebrity in an image
    
    Args:
        image_path: Path to image to analyze
        tolerance: Lower is more strict (default: 0.6)
    
    Returns:
        List of recognized celebrities with info
    """
    try:
        # Load celebrity database
        celebrity_db = load_celebrity_database()
        
        if not celebrity_db:
            print("⚠️ Celebrity database is empty")
            return []
        
        # Load and analyze image
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        
        recognized = []
        
        for face_encoding in face_encodings:
            # Compare with all celebrities in database
            for name, known_encoding in celebrity_db.items():
                # Calculate face distance
                distance = face_recognition.face_distance([known_encoding], face_encoding)[0]
                
                # If match found
                if distance < tolerance:
                    # Get Wikipedia info
                    info = get_celebrity_info(name)
                    
                    recognized.append({
                        'name': name,
                        'confidence': round((1 - distance) * 100, 2),
                        'info': info
                    })
                    break
        
        return recognized
    
    except Exception as e:
        print(f"Error recognizing celebrity: {str(e)}")
        return []

def get_celebrity_info(name):
    """
    Get celebrity information from Wikipedia
    
    Args:
        name: Celebrity name
    
    Returns:
        Dictionary with celebrity info
    """
    try:
        # Set Wikipedia language
        wikipedia.set_lang('en')
        
        # Search for the person
        search_results = wikipedia.search(name, results=1)
        
        if search_results:
            # Get page
            page = wikipedia.page(search_results[0], auto_suggest=False)
            
            # Get summary (first 3 sentences)
            summary = wikipedia.summary(name, sentences=3, auto_suggest=False)
            
            return {
                'title': page.title,
                'summary': summary,
                'url': page.url,
                'categories': page.categories[:5] if hasattr(page, 'categories') else []
            }
    
    except wikipedia.exceptions.DisambiguationError as e:
        # Multiple results, take first one
        try:
            page = wikipedia.page(e.options[0])
            summary = wikipedia.summary(e.options[0], sentences=3)
            return {
                'title': page.title,
                'summary': summary,
                'url': page.url,
                'categories': []
            }
        except:
            pass
    
    except Exception as e:
        print(f"Error getting Wikipedia info: {str(e)}")
    
    # Fallback
    return {
        'title': name,
        'summary': f"{name} - Information not available",
        'url': None,
        'categories': []
    }

def auto_detect_celebrity_type(summary, categories):
    """
    Automatically categorize celebrity based on Wikipedia info
    
    Returns:
        Category: actor, athlete, musician, politician, etc.
    """
    summary_lower = summary.lower()
    categories_str = ' '.join(categories).lower()
    
    # Check categories and summary
    if any(word in summary_lower or word in categories_str for word in ['actor', 'actress', 'film', 'movie', 'cinema']):
        return '🎬 Actor/Actress'
    
    elif any(word in summary_lower or word in categories_str for word in ['singer', 'musician', 'band', 'album', 'music']):
        return '🎵 Musician/Singer'
    
    elif any(word in summary_lower or word in categories_str for word in ['athlete', 'sport', 'football', 'cricket', 'tennis', 'basketball']):
        return '⚽ Athlete'
    
    elif any(word in summary_lower or word in categories_str for word in ['politician', 'president', 'minister', 'senator']):
        return '🏛️ Politician'
    
    elif any(word in summary_lower or word in categories_str for word in ['entrepreneur', 'ceo', 'founder', 'business']):
        return '💼 Entrepreneur'
    
    elif any(word in summary_lower or word in categories_str for word in ['influencer', 'youtuber', 'social media', 'content creator']):
        return '📱 Influencer'
    
    elif any(word in summary_lower or word in categories_str for word in ['scientist', 'researcher', 'professor']):
        return '🔬 Scientist'
    
    else:
        return '⭐ Celebrity'

"""
Vision API Routes - Complete Version with Fixed Audio
"""
from flask import Blueprint, request, jsonify, send_from_directory, send_file, make_response
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime

from app.models.object_detection import detect_objects, get_description
from app.models.face_recognition import recognize_faces
from app.models.translation import translate_text
from app.models.speech import generate_speech

bp = Blueprint('vision', __name__)

@bp.route('/upload', methods=['POST'])
def upload_image():
    '''Handle image upload'''
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file:
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            filepath = os.path.join('uploads', unique_filename)
            file.save(filepath)
            
            return jsonify({
                'success': True,
                'filename': unique_filename,
                'filepath': filepath
            }), 200
        
        return jsonify({'error': 'Invalid file type'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/analyze', methods=['POST'])
def analyze_image():
    '''Analyze uploaded image - Complete working version'''
    try:
        data = request.get_json()
        filepath = data.get('filepath')
        
        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'Image file not found'}), 404
        
        print(f"Starting analysis for: {filepath}")
        
        # STEP 1: YOLOv8 Object Detection
        detected_objects = detect_objects(filepath)
        print(f"Detected {len(detected_objects)} objects")
        
        # STEP 2: Generate annotated image with bounding boxes
        annotated_image_path = None
        try:
            from app.models.image_annotator import draw_bounding_boxes
            if detected_objects:
                annotated_image_path = draw_bounding_boxes(filepath, detected_objects)
                print(f"Annotated image: {annotated_image_path}")
        except Exception as e:
            print(f"Annotation warning: {e}")
        
        # STEP 3: Face Recognition (always try, but track if YOLO saw a person)
        recognized_faces = []
        person_detected = any(obj['class'].lower() == 'person' for obj in detected_objects)
        
        try:
            recognized_faces = recognize_faces(filepath)
            print(f"Found {len(recognized_faces)} faces")
        except Exception as e:
            print(f"Face recognition warning: {e}")
        
        # STEP 4: Generate detailed scene description
        try:
            from app.models.scene_description import generate_detailed_scene_description
            detailed_description = generate_detailed_scene_description(
                detected_objects, 
                recognized_faces, 
                filepath
            )
        except Exception as e:
            print(f"Scene description warning: {e}")
            # Fallback description
            detailed_description = {
                'full_description': get_description(detected_objects),
                'line_count': 1,
                'description_lines': [get_description(detected_objects)],
                'has_celebrity': False
            }
        
        # STEP 5: Generate shopping links
        shopping_data = {}
        try:
            from app.models.shopping import get_shopping_links_with_description
            shopping_data = get_shopping_links_with_description(detected_objects)
        except Exception as e:
            print(f"Shopping links warning: {e}")
        
        # Combine results
        results = {
            'objects': detected_objects,
            'faces': recognized_faces,
            'person_detected': person_detected,
            'detailed_description': detailed_description,
            'shopping_links': shopping_data,
            'original_image': filepath,
            'annotated_image': annotated_image_path,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(results), 200
    
    except Exception as e:
        print(f"Analysis error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@bp.route('/translate', methods=['POST'])
def translate():
    '''Translate text to multiple languages'''
    try:
        data = request.get_json()
        text = data.get('text')
        target_languages = data.get('languages', ['te', 'hi', 'es'])
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        print(f"Translating to: {target_languages}")
        
        translations = {}
        for lang in target_languages:
            try:
                translated = translate_text(text, target_lang=lang)
                translations[lang] = translated
                print(f"✓ {lang}: {translated[:50]}...")
            except Exception as e:
                print(f"Translation error for {lang}: {e}")
                translations[lang] = text
        
        return jsonify({
            'original': text,
            'translations': translations
        }), 200
    
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/speak', methods=['POST'])
def speak():
    '''Generate speech from text'''
    try:
        data = request.get_json()
        text = data.get('text')
        language = data.get('language', 'en')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        print(f"[{language}] Speech request for: {text[:50]}...")
        
        audio_file = generate_speech(text, language)
        
        if audio_file:
            print(f"[{language}] ✓ Audio generated: {audio_file}")
            return jsonify({
                'success': True,
                'audio_file': audio_file
            }), 200
        else:
            print(f"[{language}] ✗ Audio generation failed")
            return jsonify({
                'success': False,
                'error': 'Failed to generate audio'
            }), 500
    
    except Exception as e:
        print(f"Speech error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/audio/<filename>')
def serve_audio(filename):
    '''Serve audio file with proper headers - FIXED VERSION'''
    try:
        # Construct full path
        audio_path = os.path.join('static', 'audio', filename)
        
        print(f"Audio request: {filename}")
        print(f"Absolute path: {os.path.abspath(audio_path)}")
        print(f"File exists: {os.path.exists(audio_path)}")
        
        # Check if file exists
        if not os.path.exists(audio_path):
            print(f"✗ File not found: {audio_path}")
            # List available files for debugging
            audio_dir = os.path.join('static', 'audio')
            if os.path.exists(audio_dir):
                available = os.listdir(audio_dir)
                print(f"Available files: {available[:5]}")
            return jsonify({'error': 'Audio file not found'}), 404
        
        # Get file size
        file_size = os.path.getsize(audio_path)
        print(f"✓ Serving: {audio_path} ({file_size} bytes)")
        
        # Send file directly with proper headers
        return send_file(
            audio_path,
            mimetype='audio/mpeg',
            as_attachment=False,
            download_name=filename
        )
        
    except Exception as e:
        print(f"✗ Audio serve error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@bp.route('/shopping', methods=['POST'])
def get_shopping():
    '''Get shopping links for objects'''
    try:
        from app.models.shopping import get_shopping_links
        
        data = request.get_json()
        objects = data.get('objects', [])
        
        links = get_shopping_links(objects)
        
        return jsonify(links), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/save', methods=['POST'])
def save_analysis():
    '''Save analysis result to Firebase'''
    try:
        from firebase.firestore_service import save_result
        
        data = request.get_json()
        result_id = save_result(data)
        
        return jsonify({'success': True, 'id': result_id}), 200
    except Exception as e:
        print(f"Save error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

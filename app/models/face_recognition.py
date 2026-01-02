from deepface import DeepFace
import os
import wikipedia
import cv2

FACE_DB_PATH = "app/models/face_db"

# Load all candidate comparison images
def get_gallery():
    if not os.path.exists(FACE_DB_PATH):
        os.makedirs(FACE_DB_PATH, exist_ok=True)
        print(f"Face gallery directory created at: {FACE_DB_PATH}")
        return []
    gallery = []
    for fname in os.listdir(FACE_DB_PATH):
        if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            gallery.append({
                'name': fname.rsplit('.', 1)[0].replace('_', ' ').title(),
                'path': os.path.join(FACE_DB_PATH, fname)
            })
    if not gallery:
        print(f"No reference faces found in {FACE_DB_PATH}")
    else:
        print(f"Loaded {len(gallery)} reference faces from {FACE_DB_PATH}")
    return gallery

def recognize_faces(image_path):
    # Quick sanity check with classical face detector to avoid false positives on non-face images
    img = cv2.imread(image_path)
    if img is None:
        print(f"Face recognition: cannot read image {image_path}")
        return []
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    detected = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
    
    if len(detected) == 0:
        print("Face recognition: no human faces detected by OpenCV; skipping DeepFace analysis")
        return []
    
    faces = DeepFace.analyze(img_path=image_path,
                             actions=['age', 'gender', 'emotion'],
                             enforce_detection=False)
    if not isinstance(faces, list):
        faces = [faces]
    recognized_faces = []
    gallery = get_gallery()
    for idx, face in enumerate(faces):
        best_match = None
        best_score = 100
        best_result = None
        for candidate in gallery:
            try:
                result = DeepFace.verify(image_path, candidate['path'], enforce_detection=False)
                if result['verified'] and result['distance'] < best_score:
                    best_score = result['distance']
                    best_match = candidate
                    best_result = result
            except Exception:
                continue
        if best_match:
            name = best_match['name']
            is_celebrity = True
            if best_result and 'distance' in best_result:
                distance = best_result['distance']
                confidence = max(0, min(100, (1 - float(distance)) * 100))
            else:
                confidence = 90.0
            try:
                summary = wikipedia.summary(name, sentences=2)
                page = wikipedia.page(name)
                wiki_info = {'summary': summary, 'url': page.url}
            except Exception:
                wiki_info = {'summary': 'No Wikipedia information available.', 'url': ''}
        else:
            name = None
            wiki_info = None
            is_celebrity = False
            confidence = None
        face_data = {
            'age': face.get('age'),
            'gender': face.get('dominant_gender'),
            'emotion': face.get('dominant_emotion'),
            'celebrity_name': name,
            'celebrity_info': wiki_info,
            'is_celebrity': is_celebrity,
            'celebrity_category': 'Celebrity' if is_celebrity else None,
            'celebrity_confidence': confidence
        }
        recognized_faces.append(face_data)
    return recognized_faces

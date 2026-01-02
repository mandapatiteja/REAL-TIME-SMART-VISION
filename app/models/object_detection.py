"""
Enhanced Object Detection with PyTorch 2.6 Compatibility
"""
from ultralytics import YOLO
import cv2
import os
import torch
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Fix for PyTorch 2.6 compatibility
try:
    torch.serialization.add_safe_globals(['ultralytics.nn.tasks.DetectionModel'])
except:
    # Alternative fix
    import torch.serialization
    torch.serialization._weights_only_unpickler_DEFAULT = False

# Global model instance
model = None

def load_model():
    """Load YOLO model with proper error handling"""
    global model
    if model is None:
        try:
            print("Loading YOLOv8 model...")
            model = YOLO('yolov8n.pt')
            print("✓ YOLOv8 model loaded successfully")
        except Exception as e:
            print(f"Error loading YOLO model: {str(e)}")
            raise
    return model

def detect_objects(image_path, confidence=0.25):
    """
    Detect objects using YOLOv8
    
    Args:
        image_path: Path to image
        confidence: Confidence threshold (default: 0.25)
    
    Returns:
        List of detected objects with bounding boxes
    """
    try:
        # Load model
        model = load_model()
        
        # Check if image exists
        if not os.path.exists(image_path):
            print(f"✗ Image not found: {image_path}")
            return []
        
        # Verify image is readable
        img = cv2.imread(image_path)
        if img is None:
            print(f"✗ Cannot read image: {image_path}")
            return []
        
        print(f"✓ Processing image: {image_path} ({img.shape})")
        
        # Run detection
        results = model(image_path, conf=confidence)
        
        detected_objects = []
        
        for result in results:
            boxes = result.boxes
            if boxes is not None and len(boxes) > 0:
                print(f"✓ Detected {len(boxes)} objects")
                
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    conf = float(box.conf[0])
                    cls = int(box.cls[0])
                    class_name = model.names[cls]
                    
                    detected_objects.append({
                        'class': class_name,
                        'confidence': conf,
                        'bbox': [int(x1), int(y1), int(x2), int(y2)]
                    })
                    
                    print(f"  - {class_name}: {conf*100:.1f}%")
            else:
                print("⚠ No objects detected in this result batch")
        
        # Fallback: if model did not return any objects, treat whole image as a generic object
        if not detected_objects:
            h, w = img.shape[:2]
            print("⚠ Model did not recognize any known classes; adding a generic object region covering the image")
            detected_objects.append({
                'class': 'object',
                'confidence': 0.4,
                'bbox': [0, 0, w, h]
            })
        
        return detected_objects
    
    except Exception as e:
        print(f"✗ Detection error: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

def get_description(detected_objects):
    '''Generate natural language description of detected objects'''
    if not detected_objects:
        return "No objects detected in the image."
    
    # Count objects
    object_counts = {}
    for obj in detected_objects:
        class_name = obj['class']
        object_counts[class_name] = object_counts.get(class_name, 0) + 1
    
    # Generate description
    descriptions = []
    for obj_class, count in object_counts.items():
        if count == 1:
            descriptions.append(f"a {obj_class}")
        else:
            descriptions.append(f"{count} {obj_class}s")
    
    if len(descriptions) == 1:
        return f"I can see {descriptions[0]} in this image."
    elif len(descriptions) == 2:
        return f"I can see {descriptions[0]} and {descriptions[1]} in this image."
    else:
        return f"I can see {', '.join(descriptions[:-1])}, and {descriptions[-1]} in this image."

"""
Image Annotator - Draw Bounding Boxes on Detected Objects
"""
import cv2
import numpy as np
import os

def draw_bounding_boxes(image_path, detected_objects, output_path=None):
    """
    Draw bounding boxes on image with labels
    
    Args:
        image_path: Path to original image
        detected_objects: List of detected objects with bounding boxes
        output_path: Path to save annotated image (optional)
    
    Returns:
        Path to annotated image
    """
    try:
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            print(f"Cannot read image: {image_path}")
            return None
        
        # Create output path if not provided
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = os.path.join('uploads', f'{base_name}_annotated.jpg')
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Color map for different object classes
        color_map = {
            'person': (0, 255, 0),      # Green
            'car': (255, 0, 0),         # Blue
            'chair': (0, 0, 255),       # Red
            'bottle': (255, 255, 0),    # Cyan
            'laptop': (255, 0, 255),    # Magenta
            'tv': (0, 255, 255),        # Yellow
            'book': (128, 0, 128),      # Purple
            'cell phone': (255, 165, 0), # Orange
        }
        
        # Draw each bounding box
        for obj in detected_objects:
            class_name = obj['class']
            confidence = obj['confidence']
            bbox = obj['bbox']
            
            # Get coordinates
            x1, y1, x2, y2 = bbox
            
            # Get color for this class (default to green)
            color = color_map.get(class_name, (0, 255, 0))
            
            # Draw rectangle
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
            
            # Prepare label text
            label = f'{class_name} {confidence*100:.1f}%'
            
            # Get text size for background
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.7
            thickness = 2
            (text_width, text_height), baseline = cv2.getTextSize(label, font, font_scale, thickness)
            
            # Draw background rectangle for text
            cv2.rectangle(img, 
                         (x1, y1 - text_height - 10), 
                         (x1 + text_width + 10, y1), 
                         color, 
                         -1)
            
            # Draw text
            cv2.putText(img, label, 
                       (x1 + 5, y1 - 5), 
                       font, font_scale, 
                       (255, 255, 255), 
                       thickness)
        
        # Save annotated image
        cv2.imwrite(output_path, img)
        print(f"✓ Annotated image saved: {output_path}")
        
        return output_path
    
    except Exception as e:
        print(f"Error annotating image: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

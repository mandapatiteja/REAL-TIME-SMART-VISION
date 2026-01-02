"""
Detailed Scene Description Generator
"""

def generate_detailed_scene_description(detected_objects, recognized_faces, image_path):
    """
    Generate a detailed description of the scene
    
    Args:
        detected_objects: List of detected objects from YOLO
        recognized_faces: List of recognized faces from DeepFace
        image_path: Path to analyzed image
    
    Returns:
        Dictionary with detailed descriptions
    """
    description_lines = []
    
    # Count objects
    object_counts = {}
    for obj in detected_objects:
        obj_class = obj['class']
        object_counts[obj_class] = object_counts.get(obj_class, 0) + 1
    
    # === LINE 1-2: Overall Scene Summary ===
    total_objects = len(detected_objects)
    total_people = object_counts.get('person', 0)
    
    if total_people > 0:
        description_lines.append(
            f"This image contains {total_people} {'person' if total_people == 1 else 'people'} "
            f"along with {total_objects - total_people} other objects in the scene."
        )
    else:
        description_lines.append(
            f"This image shows a scene with {total_objects} detected objects. "
            f"No people are visible in this image."
        )
    
    # === LINE 3-5: Celebrity/Person Details ===
    if recognized_faces and len(recognized_faces) > 0:
        for idx, face in enumerate(recognized_faces):
            if face.get('is_celebrity') and face.get('celebrity_info'):
                celeb_name = face['celebrity_name']
                celeb_category = face.get('celebrity_category', 'Celebrity')
                celeb_info = face['celebrity_info']
                
                description_lines.append(
                    f"The person in the image is identified as {celeb_name}, "
                    f"categorized as {celeb_category}."
                )
                
                # Add Wikipedia summary
                if celeb_info.get('summary'):
                    description_lines.append(celeb_info['summary'])
                
                # Add Wikipedia link
                if celeb_info.get('url'):
                    description_lines.append(
                        f"For more information about {celeb_name}, "
                        f"visit: {celeb_info['url']}"
                    )
            else:
                # Non-celebrity person description
                gender = face.get('gender', 'person')
                age = face.get('age', 'unknown age')
                emotion = face.get('emotion', 'neutral')
                
                description_lines.append(
                    f"Person {idx + 1}: A {emotion} {gender} who appears to be around {age} years old. "
                    f"This individual is not recognized as a public figure or celebrity in our database."
                )
    
    # === LINE 6-8: Objects and Environment ===
    if len(object_counts) > 1:  # More than just people
        non_person_objects = {k: v for k, v in object_counts.items() if k != 'person'}
        
        if non_person_objects:
            description_lines.append(
                "The scene also contains the following objects:"
            )
            
            object_descriptions = []
            for obj_name, count in list(non_person_objects.items())[:5]:  # Top 5 objects
                if count == 1:
                    object_descriptions.append(f"a {obj_name}")
                else:
                    object_descriptions.append(f"{count} {obj_name}s")
            
            description_lines.append(
                f"{', '.join(object_descriptions[:-1])}, and {object_descriptions[-1]}."
            )
    
    # === LINE 9-10: Context and Scenario ===
    scenario = analyze_scenario(object_counts, recognized_faces)
    description_lines.append(scenario)
    
    # === LINE 11+: Additional Details ===
    if total_objects > 5:
        description_lines.append(
            f"This is a complex scene with multiple elements. "
            f"The composition suggests a {get_scene_type(object_counts)} setting."
        )
    
    # Add confidence
    if detected_objects:
        avg_confidence = sum(obj['confidence'] for obj in detected_objects) / len(detected_objects)
        description_lines.append(
            f"The detection system analyzed this image with an average confidence of {avg_confidence*100:.1f}%, "
            f"identifying objects across various categories with high accuracy."
        )
    
    return {
        'full_description': ' '.join(description_lines),
        'line_count': len(description_lines),
        'description_lines': description_lines,
        'has_celebrity': any(f.get('is_celebrity') for f in recognized_faces) if recognized_faces else False,
        'scene_type': get_scene_type(object_counts)
    }

def analyze_scenario(object_counts, recognized_faces):
    """Analyze and describe the likely scenario"""
    
    # Indoor vs Outdoor detection
    outdoor_objects = {'car', 'truck', 'bus', 'bicycle', 'motorcycle', 'traffic light'}
    indoor_objects = {'tv', 'laptop', 'mouse', 'keyboard', 'chair', 'couch', 'bed'}
    
    outdoor_count = sum(count for obj, count in object_counts.items() if obj in outdoor_objects)
    indoor_count = sum(count for obj, count in object_counts.items() if obj in indoor_objects)
    
    if outdoor_count > indoor_count:
        scenario = "Based on the detected objects, this appears to be an outdoor scene, possibly on a street, park, or public area."
    elif indoor_count > outdoor_count:
        scenario = "The composition suggests this is an indoor setting, likely within a home, office, or enclosed space."
    else:
        scenario = "This scene contains a mix of elements that could indicate either an indoor-outdoor transition or a semi-enclosed environment."
    
    # Activity detection
    if 'person' in object_counts:
        if object_counts['person'] > 1:
            scenario += " Multiple people are present, suggesting a social gathering, meeting, or public event."
        else:
            scenario += " A single individual is captured, possibly in a portrait or candid moment."
    
    return scenario

def get_scene_type(object_counts):
    """Determine the type of scene"""
    
    if 'person' in object_counts and object_counts['person'] >= 2:
        return "social or group"
    elif any(obj in object_counts for obj in ['car', 'bus', 'truck']):
        return "urban or transportation"
    elif any(obj in object_counts for obj in ['couch', 'bed', 'chair', 'tv']):
        return "residential or home"
    elif any(obj in object_counts for obj in ['laptop', 'keyboard', 'mouse']):
        return "workspace or office"
    else:
        return "general"

"""
Shopping Link Generator with Descriptions
"""
from urllib.parse import quote

def get_shopping_links_with_description(detected_objects):
    """
    Generate shopping links with detailed descriptions for each object
    
    Args:
        detected_objects: List of detected objects from YOLO
    
    Returns:
        Dictionary with object shopping data and descriptions
    """
    shopping_data = {}
    
    # Get unique objects (excluding 'person')
    unique_objects = {}
    for obj in detected_objects:
        obj_class = obj['class']
        if obj_class.lower() != 'person':
            if obj_class not in unique_objects:
                unique_objects[obj_class] = {
                    'count': 1,
                    'confidence': obj['confidence']
                }
            else:
                unique_objects[obj_class]['count'] += 1
    
    # Generate shopping links and descriptions for each object
    for obj_name, obj_data in unique_objects.items():
        count = obj_data['count']
        confidence = obj_data['confidence']
        
        shopping_data[obj_name] = {
            'name': obj_name,
            'count': count,
            'confidence': round(confidence * 100, 1),
            'description': generate_object_description(obj_name, count),
            'shopping_links': [
                {
                    'name': 'Amazon',
                    'url': f"https://www.amazon.com/s?k={quote(obj_name)}",
                    'icon': '🛒',
                    'description': f"Search for {obj_name} on Amazon - Free shipping available"
                },
                {
                    'name': 'eBay',
                    'url': f"https://www.ebay.com/sch/i.html?_nkw={quote(obj_name)}",
                    'icon': '💼',
                    'description': f"Find {obj_name} deals on eBay - New and used options"
                },
                {
                    'name': 'Walmart',
                    'url': f"https://www.walmart.com/search?q={quote(obj_name)}",
                    'icon': '🏬',
                    'description': f"Shop {obj_name} at Walmart - Everyday low prices"
                }
            ]
        }
    
    return shopping_data

def generate_object_description(object_name, count):
    """Generate descriptive text for detected objects"""
    
    object_descriptions = {
        'car': "A motor vehicle detected in the image.",
        'chair': "Seating furniture designed for one person.",
        'laptop': "A portable computer device.",
        'cell phone': "A mobile communication device.",
        'book': "A written or printed work consisting of pages.",
        'bottle': "A container typically used for liquids.",
        'cup': "A small container for drinking.",
        'tv': "A television set for viewing broadcast programs.",
    }
    
    # Get description or generate generic one
    base_description = object_descriptions.get(
        object_name.lower(),
        f"A {object_name} detected in the image."
    )
    
    # Add count information
    if count > 1:
        return f"{count} {object_name}s detected. {base_description}"
    else:
        return f"One {object_name} detected. {base_description}"

def get_shopping_links(objects):
    """Legacy function for backward compatibility"""
    links = {}
    
    for obj_name in objects:
        links[obj_name] = [
            {
                'name': 'Amazon',
                'url': f"https://www.amazon.com/s?k={quote(obj_name)}",
                'icon': 'https://www.amazon.com/favicon.ico'
            },
            {
                'name': 'eBay',
                'url': f"https://www.ebay.com/sch/i.html?_nkw={quote(obj_name)}",
                'icon': 'https://www.ebay.com/favicon.ico'
            }
        ]
    
    return links

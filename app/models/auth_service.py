"""
Authentication Service for user management
"""
from firebase.firebase_admin_setup import get_firestore_client
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

def create_user(email, password, name=None):
    '''
    Create a new user account
    
    Args:
        email: User email address
        password: User password (will be hashed)
        name: Optional user name
    
    Returns:
        Dictionary with user data or None if creation fails
    '''
    try:
        db = get_firestore_client()
        if db is None:
            return None
        
        # Check if user already exists
        users_ref = db.collection('users')
        existing_user = users_ref.where('email', '==', email).limit(1).stream()
        
        if list(existing_user):
            return None  # User already exists
        
        # Create new user
        user_id = str(uuid.uuid4())
        user_data = {
            'id': user_id,
            'email': email,
            'password_hash': generate_password_hash(password),
            'name': name or email.split('@')[0],
            'created_at': datetime.now(),
            'last_login': None
        }
        
        users_ref.document(user_id).set(user_data)
        return {
            'id': user_id,
            'email': user_data['email'],
            'name': user_data['name']
        }
    
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        return None

def authenticate_user(email, password):
    '''
    Authenticate a user with email and password
    
    Args:
        email: User email address
        password: User password
    
    Returns:
        Dictionary with user data if authentication succeeds, None otherwise
    '''
    try:
        db = get_firestore_client()
        if db is None:
            return None
        
        # Find user by email
        users_ref = db.collection('users')
        users = users_ref.where('email', '==', email).limit(1).stream()
        
        user_doc = None
        for doc in users:
            user_doc = doc
            break
        
        if not user_doc:
            return None
        
        user_data = user_doc.to_dict()
        
        # Verify password
        if check_password_hash(user_data.get('password_hash', ''), password):
            # Update last login
            user_doc.reference.update({'last_login': datetime.now()})
            
            return {
                'id': user_data.get('id'),
                'email': user_data.get('email'),
                'name': user_data.get('name')
            }
        
        return None
    
    except Exception as e:
        print(f"Error authenticating user: {str(e)}")
        return None

def get_user_by_id(user_id):
    '''
    Get user data by user ID
    
    Args:
        user_id: User ID
    
    Returns:
        Dictionary with user data or None if not found
    '''
    try:
        db = get_firestore_client()
        if db is None:
            return None
        
        user_doc = db.collection('users').document(user_id).get()
        
        if user_doc.exists:
            user_data = user_doc.to_dict()
            return {
                'id': user_data.get('id'),
                'email': user_data.get('email'),
                'name': user_data.get('name')
            }
        
        return None
    
    except Exception as e:
        print(f"Error getting user: {str(e)}")
        return None






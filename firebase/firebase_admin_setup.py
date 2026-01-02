"""
Firebase Admin SDK Setup
"""
import firebase_admin
from firebase_admin import credentials, firestore
import os
from config import Config

# Initialize Firebase Admin SDK
def initialize_firebase():
    '''Initialize Firebase Admin SDK with service account credentials'''
    try:
        # Check if already initialized
        if not firebase_admin._apps:
            cred_path = Config.FIREBASE_CREDENTIALS
            
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                print("Firebase initialized successfully")
            else:
                print(f"Warning: Firebase credentials not found at {cred_path}")
                print("Firebase features will be disabled")
                return None
        
        return firestore.client()
    
    except Exception as e:
        print(f"Error initializing Firebase: {str(e)}")
        return None

# Get Firestore client
def get_firestore_client():
    '''Get Firestore database client'''
    try:
        return firestore.client()
    except Exception as e:
        print(f"Error getting Firestore client: {str(e)}")
        return None

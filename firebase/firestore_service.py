"""
Firestore Service for storing and retrieving analysis history
"""
from firebase.firebase_admin_setup import get_firestore_client
from datetime import datetime
import uuid

def save_result(data):
    '''
    Save analysis result to Firestore
    
    Args:
        data: Dictionary containing analysis results
    
    Returns:
        Document ID of saved result
    '''
    try:
        db = get_firestore_client()
        if db is None:
            return None
        
        # Add timestamp and ID
        data['timestamp'] = datetime.now()
        data['id'] = str(uuid.uuid4())
        
        # Save to Firestore
        doc_ref = db.collection('analysis_history').document(data['id'])
        doc_ref.set(data)
        
        return data['id']
    
    except Exception as e:
        print(f"Error saving to Firestore: {str(e)}")
        return None

def get_history(limit=20):
    '''
    Get analysis history from Firestore
    
    Args:
        limit: Maximum number of results to return
    
    Returns:
        List of analysis history documents
    '''
    try:
        db = get_firestore_client()
        if db is None:
            return []
        
        # Query Firestore
        docs = db.collection('analysis_history')\
            .order_by('timestamp', direction=firestore.Query.DESCENDING)\
            .limit(limit)\
            .stream()
        
        history = []
        for doc in docs:
            data = doc.to_dict()
            history.append(data)
        
        return history
    
    except Exception as e:
        print(f"Error retrieving history: {str(e)}")
        return []

def delete_result(result_id):
    '''
    Delete a result from Firestore
    
    Args:
        result_id: ID of the result to delete
    
    Returns:
        Boolean indicating success
    '''
    try:
        db = get_firestore_client()
        if db is None:
            return False
        
        db.collection('analysis_history').document(result_id).delete()
        return True
    
    except Exception as e:
        print(f"Error deleting result: {str(e)}")
        return False

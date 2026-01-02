"""
Flask Application Factory
"""
from flask import Flask
from config import Config
import os

def create_app(config_class=Config):
    # Explicitly set template and static folders
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    app.config.from_object(config_class)
    
    # Initialize Firebase
    from firebase.firebase_admin_setup import initialize_firebase
    initialize_firebase()
    
    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('static/audio', exist_ok=True)
    os.makedirs('weights', exist_ok=True)
    
    # Register blueprints
    from app.api import main_routes, vision_routes, auth_routes
    app.register_blueprint(main_routes.bp)
    app.register_blueprint(vision_routes.bp, url_prefix='/api')
    app.register_blueprint(auth_routes.bp)
    
    return app

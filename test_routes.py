from flask import Flask, url_for
from app.api.auth_routes import bp as auth_bp
from app.api.main_routes import bp as main_bp

app = Flask(__name__)
app.secret_key = 'test_key'
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

with app.test_request_context():
    print("Building auth.guest_login...")
    print(url_for('auth.guest_login'))
    
    print("Building main.dashboard...")
    print(url_for('main.dashboard'))
    
    print("Building auth.login...")
    print(url_for('auth.login'))
    
    print("All URLs built successfully.")

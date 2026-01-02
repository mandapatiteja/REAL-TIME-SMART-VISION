from firebase.firebase_admin_setup import initialize_firebase

# Test Firebase connection
db = initialize_firebase()

if db:
    print("✅ Firebase connected successfully!")
else:
    print("❌ Firebase connection failed!")

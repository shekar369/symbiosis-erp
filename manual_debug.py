import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

print("Attempting to import app.db.session...")
try:
    import app.db.session
    print(f"Successfully imported app.db.session: {app.db.session}")
    print(f"Attributes: {dir(app.db.session)}")
except Exception as e:
    print(f"Failed to import app.db.session: {e}")
    import traceback
    traceback.print_exc()

print("\nAttempting to import SessionLocal from app.db.session...")
try:
    from app.db.session import SessionLocal
    print("Successfully imported SessionLocal")
except Exception as e:
    print(f"Failed to import SessionLocal: {e}")
    import traceback
    traceback.print_exc()

print("\nAttempting to import app.main...")
try:
    from app.main import app
    print("Successfully imported app.main")
except Exception as e:
    print(f"Failed to import app.main: {e}")
    import traceback
    traceback.print_exc()

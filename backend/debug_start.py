import sys
import os

print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")

try:
    import fastapi
    print("✓ fastapi imported")
except ImportError as e:
    print(f"✗ fastapi import failed: {e}")

try:
    import uvicorn
    print("✓ uvicorn imported")
except ImportError as e:
    print(f"✗ uvicorn import failed: {e}")

try:
    from main import app
    print("✓ main:app loaded successfully")
except Exception as e:
    print(f"✗ Failed to load main:app: {e}")
    import traceback
    traceback.print_exc()

if __name__ == "__main__":
    print("\nStarting uvicorn...")
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)

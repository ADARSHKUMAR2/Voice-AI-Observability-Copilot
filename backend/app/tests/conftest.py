import os
from pathlib import Path
import pytest
from dotenv import load_dotenv

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # Automatically locate and load the backend/.env file on your Mac host
    backend_root = Path(__file__).resolve().parents[2]
    env_path = backend_root / ".env"
    
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    
    # Override MONGO_URI to use localhost when running tests outside Docker
    # (Inside Docker the hostname 'mongo' resolves, but on the host it doesn't)
    # Force override because .env already sets it to 'mongodb://mongo:27017/voice_copilot'
    os.environ["MONGO_URI"] = "mongodb://localhost:27017/voice_copilot"

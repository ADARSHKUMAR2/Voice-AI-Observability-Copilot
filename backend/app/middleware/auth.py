from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def setup_cors_middleware(app: FastAPI) -> None:
    """Configure CORS middleware for the application.
    
    This is centralized here so all services can share the same CORS policy.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    origins = [
        "http://localhost:5000",
        "http://localhost:5001",
        "https://app.gohighlevel.com",
        
        "https://mango-sea-01234567f.azurestaticapps.net", 
        "https://yourcustomdomain.com"                     
    ]
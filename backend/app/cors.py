from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

def setup_cors(app):
    origins = [
        "http://localhost",
        f"http://127.0.0.1:{settings.fe_port}",
        settings.fe_deploy_url,
        f"http://localhost:{settings.fe_port}"
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
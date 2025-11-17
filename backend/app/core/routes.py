from fastapi import FastAPI
from app.core.config import settings  
from app.routers.api_test import (test) 
from app.routers import ( users, auth )


def register_routes(app: FastAPI):
    
    app.include_router(users.router, tags=["Users 💁🏻‍♂️"], prefix="/users")
    app.include_router(auth.router, tags=["Auth 🔑"], prefix="/auth")

    if not settings.enable_api_test_routes:
        return  
    """ routes for api test readings """
    api_prefix = "/api"
    tag = "API Test 🧪"
    app.include_router(test.router, prefix=api_prefix, tags=[tag])


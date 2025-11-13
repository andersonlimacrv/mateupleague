import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.cors import setup_cors
from app.core.routes import register_routes
from app.backend_pre_start import async_main
from app.exceptions.exceptions import (
    UsernameAlreadyExists,
    create_exception_handler,
)

app = FastAPI(default_response_class=JSONResponse)

setup_cors(app)
register_routes(app)

@app.get("/", tags=["Root 🌱"])
def read_root():
    response = {
        "message": f"Hello from {settings.APP_NAME}",
        "environment": settings.ENVIRONMENT,
    }

    if settings.ENVIRONMENT.lower() not in ["production", "prod"]:
        response["docs"] = f"http://localhost:{settings.be_port}/docs"

    return response

async def startup_event():
    await async_main()


app.add_event_handler("startup", startup_event)

app.add_exception_handler(
    exc_class_or_status_code=UsernameAlreadyExists,
    handler=create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST,
        initial_detail="Data can't be processed, check the input.",
    ),
)

def start():
    print(f"🚀 Backend running on port {settings.be_port}")
    print(f"🌐 Frontend running on port {settings.fe_port}")
    print(f"📦 Frontend DEPLOY URL: {settings.fe_deploy_url}")
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.be_port, reload=settings.ENVIRONMENT == "production", workers=2)

if __name__ == "__main__":
    start()

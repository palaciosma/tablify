# External imports
from fastapi import FastAPI

# Internal imports
from app.src.routes import router as api_routes

def create_app():
    app = FastAPI()
    app.include_router(api_routes)
    return app

app = create_app()



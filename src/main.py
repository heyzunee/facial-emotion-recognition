from fastapi import FastAPI

from .routes import route

app = FastAPI(
    title="Face emotion recognition API",
    description="API for face emotion recognition using FastAPI",
    version="1.0.0",
)

app.include_router(route.api_router)

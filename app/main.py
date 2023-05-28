from fastapi import FastAPI

from app.views.health_check import router as health_check_router


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(health_check_router)
    return application


app = get_application()

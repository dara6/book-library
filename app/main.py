from fastapi import FastAPI

from app.views import list_of_routes


def bind_routes(application: FastAPI) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route)


def get_application() -> FastAPI:
    application = FastAPI()
    bind_routes(application)
    return application


app = get_application()

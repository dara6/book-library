from app.views.health_check import api_router as application_health_router
from app.views.genres import api_router_v1 as genre_router_v1


list_of_routes = [application_health_router, genre_router_v1]

__all__ = ['list_of_routes']

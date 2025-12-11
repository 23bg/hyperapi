# racerapi/core/controller.py

from fastapi import APIRouter
import inspect


def build_router(prefix: str, controller_cls):
    router = APIRouter(prefix=f"/{prefix}")

    controller = controller_cls()  # Instantiate controller

    for name, method in inspect.getmembers(controller, inspect.ismethod):
        route_method = getattr(method, "__route_method__", None)
        route_path = getattr(method, "__route_path__", None)

        if not route_method:
            continue

        router.add_api_route(route_path, method, methods=[route_method])

    return router

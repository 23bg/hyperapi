from racerapi.core.application import Application
from racerapi.core.middleware import register_middleware
from racerapi.core.module_loader import discover_modules, load_controllers
from racerapi.core.plugins import load_plugins


def racerAPI(settings=None):
    app = Application(settings)

    register_middleware(app)

    discover_modules()
    load_controllers(app)
    load_plugins(app)

    return app.fastapi  # return real FastAPI object to ASGI server

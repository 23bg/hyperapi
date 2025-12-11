# racerapi/core/module_loader.py

import importlib
import pkgutil
from fastapi import FastAPI
from racerapi.core.registry import get_registered_controllers
from racerapi.core.controller import build_router


def discover_modules(base_package="app.modules"):
    """Auto-import all modules under app.modules."""
    try:
        package = importlib.import_module(base_package)
    except ImportError:
        print(f"❌ Could not import {base_package}")
        return

    for module in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        module_name = module.name
        try:
            importlib.import_module(module_name)
        except Exception as e:
            print(f"❌ Failed loading module {module_name}: {e}")


def load_controllers(app: FastAPI):
    for entry in get_registered_controllers():
        prefix = entry["prefix"]
        controller = entry["controller"]
        router = build_router(prefix, controller)
        app.include_router(router)
        print(f"✓ Registered Controller: {controller.__name__} → /{prefix}")

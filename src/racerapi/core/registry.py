# racerapi/core/registry.py

controller_registry = []


def register_controller(prefix: str, cls):
    controller_registry.append({
        "prefix": prefix,
        "controller": cls,
    })


def get_registered_controllers():
    return controller_registry

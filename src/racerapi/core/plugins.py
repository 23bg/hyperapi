# racerapi/core/plugins.py

import importlib_metadata


def load_plugins(app, cli_app=None):
    """Load plugins using Python entry points."""
    for ep in importlib_metadata.entry_points().get("racerapi.plugins", []):
        plugin_cls = ep.load()
        plugin = plugin_cls()

        if hasattr(plugin, "register"):
            plugin.register(app)

        if cli_app and hasattr(plugin, "register_cli"):
            plugin.register_cli(cli_app)

        if hasattr(plugin, "on_startup"):
            app.add_event_handler("startup", lambda: plugin.on_startup(app))

        if hasattr(plugin, "on_shutdown"):
            app.add_event_handler("shutdown", lambda: plugin.on_shutdown(app))

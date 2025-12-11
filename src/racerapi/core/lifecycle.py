# racerapi/core/lifecycle.py

"""
RacerAPI Lifecycle System
-------------------------

This subsystem manages all application lifecycle events including:

- Startup hooks (before accepting requests)
- Shutdown hooks (graceful teardown)
- App-ready hooks (after modules, plugins, controllers are loaded)
- Health check registry for readiness/liveness probes
- Async hook support
- Plugin and module interoperability

This enables an enterprise-scale initialization pipeline similar to:
NestJS → OnModuleInit, OnModuleDestroy
Spring → @PostConstruct, @PreDestroy
FastAPI → event handlers
Django → signals

AI-native systems also require warmup hooks, model loading, cache priming, etc.
This system provides those capabilities.
"""

import inspect
import asyncio


# ============================================================
# INTERNAL REGISTRIES
# ============================================================

STARTUP_HOOKS = []
SHUTDOWN_HOOKS = []
APP_READY_HOOKS = []
HEALTH_CHECKS = {}

MODULE_INIT_HOOKS = []
MODULE_DESTROY_HOOKS = []


# ============================================================
# UTIL: RUN SYNC/ASYNC FUNCTIONS
# ============================================================


async def _run_callable(func, *args, **kwargs):
    """Run sync or async functions transparently."""
    if inspect.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    else:
        return func(*args, **kwargs)


# ============================================================
# PUBLIC DECORATORS / REGISTRATION FUNCTIONS
# ============================================================


def on_startup(func):
    """
    Register a function to run at application startup.
    Called before serving any requests.

    Example:
        @on_startup
        def init_cache(): ...
    """
    STARTUP_HOOKS.append(func)
    return func


def on_shutdown(func):
    """
    Register a function to run during graceful shutdown.
    Useful for closing DB sessions, flushing logs, cleaning workers.
    """
    SHUTDOWN_HOOKS.append(func)
    return func


def after_app_ready(func):
    """
    Function called AFTER:
      - modules are discovered
      - controllers are registered
      - plugins are loaded

    Useful for:
      - AI model warmup
      - embedding cache preload
      - background scheduler boot
      - telemetry setup
    """
    APP_READY_HOOKS.append(func)
    return func


# ---------------- MODULE-LEVEL HOOKS ------------------------


def on_module_init(func):
    """
    Called once for each module after it is imported.
    Modules may register initialization logic here.

    Example:
        @on_module_init
        def init_users_module(): ...
    """
    MODULE_INIT_HOOKS.append(func)
    return func


def on_module_destroy(func):
    """
    Called when the app shuts down.
    Modules may clean up allocated resources.
    """
    MODULE_DESTROY_HOOKS.append(func)
    return func


# ============================================================
# HEALTH CHECK REGISTRATION
# ============================================================


def register_health_check(name: str, func):
    """
    Register a health check function. Should return:
      { "status": "ok" }
    or:
      { "status": "error", "reason": "..." }

    Integrates with system /health endpoint.
    """
    HEALTH_CHECKS[name] = func


def run_health_checks():
    """
    Execute all health checks and return aggregated results.
    """
    results = {}
    for name, check in HEALTH_CHECKS.items():
        try:
            results[name] = check()
        except Exception as e:
            results[name] = {"status": "error", "reason": str(e)}
    return results


# ============================================================
# ORCHESTRATION HELPERS — CALLED BY APP FACTORY
# ============================================================


async def execute_startup(app):
    """
    Execute startup hooks in order.
    """
    for hook in STARTUP_HOOKS:
        await _run_callable(hook, app)


async def execute_shutdown(app):
    """
    Execute shutdown hooks and module destroy hooks.
    """
    # Run module-level destroys first
    for hook in MODULE_DESTROY_HOOKS:
        await _run_callable(hook, app)

    # Then run shutdown hooks
    for hook in SHUTDOWN_HOOKS:
        await _run_callable(hook, app)


async def execute_app_ready(app):
    """
    Execute hooks that run after app is fully built,
    but before serving requests.
    """
    for hook in APP_READY_HOOKS:
        await _run_callable(hook, app)


async def execute_module_init(app):
    """
    Execute module-level initialization hooks.
    Called after module discovery.
    """
    for hook in MODULE_INIT_HOOKS:
        await _run_callable(hook, app)


# ============================================================
# INTEGRATION WITH FASTAPI APP
# ============================================================


def attach_lifecycle_events(app):
    """
    Attach the lifecycle orchestration to FastAPI’s native event system.
    Called by create_app().

    Steps:
      1. FastAPI startup triggers execute_startup()
      2. FastAPI shutdown triggers execute_shutdown()
    """

    @app.on_event("startup")
    async def _startup():
        await execute_startup(app)

    @app.on_event("shutdown")
    async def _shutdown():
        await execute_shutdown(app)

    return app

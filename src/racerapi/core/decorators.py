# racerapi/core/decorators.py

"""
Decorator system for RacerAPI

This file defines the complete metadata-driven decorator layer for RacerAPI.
These decorators do not execute behavior directly. Instead, they annotate
controller classes and methods with metadata, which the framework collects
during module discovery and converts into FastAPI routes, middleware,
permission checks, caching, guards, AI documentation, and more.

Enterprise-grade frameworks (NestJS, Spring, ASP.NET) follow this model.
RacerAPI merges that approach with Pythonic introspection.
"""

from racerapi.core.registry import register_controller


# ============================================================
# CONTROLLER DECORATOR
# ============================================================


def Controller(prefix: str = ""):
    """
    Marks a class as a controller.
    The module loader registers this class and the controller builder
    inspects its methods for route metadata.

    Example:
        @Controller("users")
        class UserController:
            ...
    """

    def wrapper(cls):
        register_controller(prefix, cls)
        return cls

    return wrapper


# ============================================================
# BASIC ROUTE DECORATORS (HTTP verbs)
# ============================================================


def Route(method: str, path: str):
    """
    Base decorator used by all HTTP method decorators.
    Stores route method and path metadata on the handler function.
    """

    def decorator(func):
        func.__route_method__ = method
        func.__route_path__ = path
        return func

    return decorator


def Get(path: str):
    return Route("GET", path)


def Post(path: str):
    return Route("POST", path)


def Put(path: str):
    return Route("PUT", path)


def Delete(path: str):
    return Route("DELETE", path)


def Patch(path: str):
    return Route("PATCH", path)


# ============================================================
# ROUTE METADATA DECORATORS — ENTERPRISE FEATURES
# ============================================================


def Middleware(mw):
    """
    Assign per-route middleware.
    Middleware executes before the handler.
    Useful for logging, metrics, request shaping, custom auth, etc.
    """

    def wrapper(func):
        func.__middleware__ = mw
        return func

    return wrapper


def UseGuard(guard):
    """
    Assign guard for authorization. Guards are functions/classes evaluated
    before route execution. They can throw errors to block route access.

    Example:
        @UseGuard(AuthGuard)
        @Get("/admin")
        def dashboard(): ...
    """

    def wrapper(func):
        func.__guard__ = guard
        return func

    return wrapper


def Roles(*roles):
    """
    Role-based access control.
    Stored as metadata. Authorization plugin reads this metadata.

    Example:
        @Roles("admin", "superadmin")
    """

    def wrapper(func):
        func.__roles__ = roles
        return func

    return wrapper


def Version(version: str):
    """
    Version the route.
    Version-aware routers prepend version to the path.

    Example:
        @Version("v2")
        @Get("/health")
        -> /v2/health
    """

    def wrapper(func):
        func.__version__ = version
        return func

    return wrapper


def Cache(ttl: int = 60):
    """
    Mark a route as cacheable.
    Caching plugins read this and set up caching logic.

    Example:
        @Cache(120)
    """

    def wrapper(func):
        func.__cache_ttl__ = ttl
        return func

    return wrapper


def RateLimit(limit: int, window: int):
    """
    Per-route rate limiting metadata.
    A rate-limiter plugin (Redis, memory, external API gateway) uses this.

    Example:
        @RateLimit(100, 60)
    """

    def wrapper(func):
        func.__rate_limit__ = {"limit": limit, "window": window}
        return func

    return wrapper


def Secure():
    """
    Mark a route as requiring HTTPS or additional security enforcement.
    Security plugin inspects this.
    """

    def wrapper(func):
        func.__secure__ = True
        return func

    return wrapper


# ============================================================
# VALIDATION & SCHEMA METADATA
# ============================================================


def Validate(schema):
    """
    Attach input schema validation.
    FastAPI already supports validation, but custom validation OR external
    AI validation plugins may read this metadata.

    Example:
        @Validate(CreateUserSchema)
    """

    def wrapper(func):
        func.__input_schema__ = schema
        return func

    return wrapper


def ResponseModel(schema):
    """
    Output schema definition for OpenAPI, AI tools, and strict typing.

    Example:
        @ResponseModel(UserOut)
    """

    def wrapper(func):
        func.__response_schema__ = schema
        return func

    return wrapper


def Summary(text: str):
    """OpenAPI summary metadata."""

    def wrapper(func):
        func.__summary__ = text
        return func

    return wrapper


def Description(text: str):
    """OpenAPI description metadata."""

    def wrapper(func):
        func.__description__ = text
        return func

    return wrapper


# ============================================================
# AI-NATIVE DECORATORS
# ============================================================


def AIDoc(prompt: str):
    """
    AI-generated documentation metadata.
    RacerAPI can generate extended documentation, tests, and code comments
    using LLMs based on this metadata.

    Example:
        @AIDoc("Explain this endpoint for developers.")
    """

    def wrapper(func):
        func.__ai_doc__ = prompt
        return func

    return wrapper


def AIValidate(prompt: str):
    """
    AI-assisted validation logic.
    AI plugins can generate validation processors for unstructured inputs.

    Example:
        @AIValidate("Ensure description is appropriate and non-toxic.")
    """

    def wrapper(func):
        func.__ai_validate__ = prompt
        return func

    return wrapper


def AIGuard(rule: str):
    """
    AI-driven authorization rule.
    This metadata is read by LLM-based policy evaluators.

    Example:
        @AIGuard("Only internal employees can access during weekdays.")
    """

    def wrapper(func):
        func.__ai_guard__ = rule
        return func

    return wrapper


# ============================================================
# OBSERVABILITY DECORATORS
# ============================================================


def Log(level: str = "info"):
    """
    Structured application logging.
    Logging plugin inspects this metadata and injects logging.

    Example:
        @Log("debug")
    """

    def wrapper(func):
        func.__log_level__ = level
        return func

    return wrapper


def Metrics(name: str):
    """
    Hook into metrics exporters (Prometheus, OpenTelemetry).

    Example:
        @Metrics("http_request_duration_seconds")
    """

    def wrapper(func):
        func.__metric_name__ = name
        return func

    return wrapper


# ============================================================
# BACKGROUND TASK DECORATOR
# ============================================================


def BackgroundTask(task_name: str):
    """
    Metadata for background job that runs AFTER route handler.
    Plugins like Celery, RQ, or custom async executor use this.

    Example:
        @BackgroundTask("send_email")
    """

    def wrapper(func):
        func.__background_task__ = task_name
        return func

    return wrapper

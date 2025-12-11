from fastapi import FastAPI


class Application:
    def __init__(self, settings):
        self._app = FastAPI(
            title=settings.title,
            version=settings.version,
            description=settings.description,
            docs_url=settings.docs_url,
            redoc_url=settings.redoc_url,
            openapi_url=settings.openapi_url,
        )

    @property
    def fastapi(self):
        return self._app

    # Abstracted convenience API:
    def add_middleware(self, *args, **kwargs):
        return self._app.add_middleware(*args, **kwargs)

    def add_exception_handler(self, *args, **kwargs):
        return self._app.add_exception_handler(*args, **kwargs)

    def include_router(self, *args, **kwargs):
        return self._app.include_router(*args, **kwargs)

    def add_event_handler(self, *args, **kwargs):
        return self._app.add_event_handler(*args, **kwargs)

# racerapi/core/container.py


class Container:
    def __init__(self):
        self._singletons = {}
        self._factories = {}

    def set(self, key: str, instance):
        """Register a singleton instance."""
        self._singletons[key] = instance

    def get(self, key: str):
        """Retrieve singleton or factory-created instance."""
        if key in self._singletons:
            return self._singletons[key]
        if key in self._factories:
            instance = self._factories[key]()
            self._singletons[key] = instance
            return instance
        return None

    def has(self, key: str) -> bool:
        return key in self._singletons or key in self._factories

    def factory(self, key: str, factory):
        """Register a factory that lazily creates the service."""
        self._factories[key] = factory


container = Container()

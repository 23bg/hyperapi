from racerapi.core.decorators import Controller, Get

@Controller("system")
class SystemRepository:
    
    @Get("/health")
    def health(self):
        pass

    
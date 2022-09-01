from django.apps import AppConfig


class PortalConfig(AppConfig):
    name = 'Portal'

    def ready(self):
        import Portal.signals
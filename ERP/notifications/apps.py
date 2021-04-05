from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = 'notifications'

    def ready(self):
        import notifications.signals

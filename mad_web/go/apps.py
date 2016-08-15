from django.apps import AppConfig


class GoConfig(AppConfig):
    name = 'mad_web.go'
    verbose_name = "Go"

    def ready(self):
        """Override this to put in:
        """
        pass

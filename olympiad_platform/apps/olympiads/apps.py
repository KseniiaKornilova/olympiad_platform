from django.apps import AppConfig


class OlympiadsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.olympiads'
    verbose_name = 'Олимпиады'

    def ready(self) -> None:
        import apps.olympiads.signals  # noqa: F401

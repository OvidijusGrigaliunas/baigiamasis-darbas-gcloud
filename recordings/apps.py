from django.apps import AppConfig


class RecordingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recordings'

    def ready(self):
        from .recordings_scheduler import data_downloader
        data_downloader.start()

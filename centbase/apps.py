from django.apps import AppConfig


class CentbaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'centbase'

    def ready(self):
        import centbase.signals
        # return super().ready()
from django.apps import AppConfig


class RoadmapConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'roadmap'
    def ready(self):
        import roadmap.signals
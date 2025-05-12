from django.apps import AppConfig

class TodoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todo'

    def ready(self):
        import todo.signals  # 👈 importa i signals quando l'app è pronta

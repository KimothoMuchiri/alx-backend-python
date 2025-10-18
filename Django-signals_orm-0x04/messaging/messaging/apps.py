from django.apps import AppConfig

class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging' # Replace 'app_name' with your actual app name

    def ready(self):
        # 💡 MANDATORY STEP: Import signals here to ensure they are registered
        import messaging.signals 
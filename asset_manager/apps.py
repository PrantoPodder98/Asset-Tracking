from django.apps import AppConfig


class AssetManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'asset_manager'

    def ready(self):
        import asset_tracking.signals  # This line is for configuring signals

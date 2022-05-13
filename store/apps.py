from django.apps import AppConfig


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    # I add this function to import all the signals in signals.py inside the store app so they are ready to be executed. Without doing this passage the functions in signals.py would be completely unknown to the all project 
    def ready(self) -> None:
        import store.signals

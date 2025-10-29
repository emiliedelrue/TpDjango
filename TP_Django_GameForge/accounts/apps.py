from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'Gestion des comptes'

    def ready(self):
        """
        Import des signals lors du démarrage de l'application
        """
        import accounts.models  # noqa
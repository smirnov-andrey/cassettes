from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CollectionManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collection_management'
    verbose_name = _('collections management')

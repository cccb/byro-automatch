from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class PluginApp(AppConfig):
    name = 'byro_automatch'
    verbose_name = 'Advanced machine learning for byro.'

    class ByroPluginMeta:
        name = ugettext_lazy('Advanced machine learning for byro.')
        author = 'Annika.'
        description = ugettext_lazy('Automatically match transactions and create bookings.')
        visible = True
        version = '0.0.1'

    def ready(self):
        from . import signals  # NOQA


default_app_config = 'byro_automatch.PluginApp'

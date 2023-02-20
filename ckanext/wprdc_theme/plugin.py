import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class WPRDCThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'wprdc_theme')
        toolkit.add_resource('assets', 'wprdc_theme')

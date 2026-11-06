import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.wprdctheme.canonical_view import (
    canonical_view_validator,
    wprdc_canonical_view,
    wprdc_canonical_view_options,
)


class WPRDCThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IValidators)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'wprdctheme')
        toolkit.add_resource('assets', 'wprdctheme')

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'wprdc_canonical_view': wprdc_canonical_view,
            'wprdc_canonical_view_options': wprdc_canonical_view_options,
        }

    # IValidators
    def get_validators(self):
        return {'wprdc_canonical_view': canonical_view_validator}

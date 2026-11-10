"""The plugin's registrations and the canonical view snippet on the dataset page."""

import pytest
from ckan.plugins import toolkit

from ckanext.wprdctheme import canonical_view
from ckanext.wprdctheme.canonical_view import FIELD_NAME
from ckanext.wprdctheme.plugin import WPRDCThemePlugin

SNIPPET = "wprdctheme/snippets/canonical_view.html"


class TestRegistrations:
    def test_helpers(self):
        helpers = WPRDCThemePlugin().get_helpers()
        assert helpers["wprdc_canonical_view"] is canonical_view.wprdc_canonical_view
        assert (
            helpers["wprdc_canonical_view_options"]
            is canonical_view.wprdc_canonical_view_options
        )

    def test_validator(self):
        validators = WPRDCThemePlugin().get_validators()
        assert validators["wprdc_canonical_view"] is canonical_view.canonical_view_validator


@pytest.mark.ckan_config("ckan.plugins", "wprdctheme image_view")
@pytest.mark.usefixtures("with_plugins", "with_request_context")
class TestCanonicalViewSnippet:
    """Uses image_view as the canonical view: it's in core and needs no data."""

    @pytest.fixture
    def pkg(self):
        return {
            "id": "pkg-1",
            "name": "bridges",
            "type": "dataset",
            "resources": [
                {"id": "res-1", "name": "Bridge photo", "url": "https://example.org/b.png"}
            ],
        }

    @pytest.fixture
    def image_view(self, monkeypatch):
        view = {
            "id": "view-1",
            "resource_id": "res-1",
            "package_id": "pkg-1",
            "view_type": "image_view",
            "title": "Photo",
            "description": "",
            "image_url": "https://example.org/b.png",
        }

        def resource_view_show(context, data_dict):
            if data_dict["id"] != view["id"]:
                raise toolkit.ObjectNotFound()
            return view

        monkeypatch.setattr(
            canonical_view.toolkit,
            "get_action",
            lambda name: {"resource_view_show": resource_view_show}[name],
        )
        return view

    def render(self, pkg):
        return toolkit.render_snippet(SNIPPET, {"pkg": pkg})

    def test_renders_view_with_heading(self, pkg, image_view):
        pkg[FIELD_NAME] = "view-1"
        html = self.render(pkg)

        assert 'class="canonical-view' in html
        assert "Photo" in html
        # heading links to the view on its resource page
        assert "/dataset/bridges/resource/res-1?view_id=view-1" in html
        assert "Bridge photo" in html
        # the view itself, via CKAN's resource_view snippet
        assert 'id="view-view-1"' in html
        assert "https://example.org/b.png" in html

    def test_nothing_when_not_set(self, pkg, image_view):
        assert "canonical-view" not in self.render(pkg)

    def test_nothing_when_view_is_gone(self, pkg, image_view):
        pkg[FIELD_NAME] = "deleted-view"
        assert "canonical-view" not in self.render(pkg)

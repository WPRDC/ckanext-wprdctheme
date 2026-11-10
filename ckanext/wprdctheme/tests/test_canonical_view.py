"""Canonical view: the validator and the template helpers.

The model and actions are faked, so these run without any data.
"""
from types import SimpleNamespace

import pytest
from ckan.lib.navl.dictization_functions import StopOnError
from ckan.plugins import toolkit

from ckanext.wprdctheme import canonical_view
from ckanext.wprdctheme.canonical_view import (
    FIELD_NAME,
    canonical_view_validator,
    wprdc_canonical_view,
    wprdc_canonical_view_options,
)

# toolkit._ and toolkit.h need a request context
pytestmark = pytest.mark.usefixtures("with_request_context")

KEY = (FIELD_NAME,)


class FakeTable:
    """Stands in for a model class: ``get`` looks up by id."""

    def __init__(self, *rows):
        self.rows = {row.id: row for row in rows}

    def get(self, id_):
        return self.rows.get(id_)


def fake_model(packages=(), resources=(), views=()):
    return SimpleNamespace(
        Package=FakeTable(*packages),
        Resource=FakeTable(*resources),
        ResourceView=FakeTable(*views),
    )


def package(id_="pkg-1", **extras):
    return SimpleNamespace(id=id_, extras=extras)


def resource(id_="res-1", package_id="pkg-1", state="active"):
    return SimpleNamespace(id=id_, package_id=package_id, state=state)


def view(id_="view-1", resource_id="res-1"):
    return SimpleNamespace(id=id_, resource_id=resource_id)


def validate(value, model, package_id="pkg-1"):
    data = {KEY: value, ("id",): package_id}
    errors = {KEY: []}
    stopped = False
    try:
        canonical_view_validator(KEY, data, errors, {"model": model})
    except StopOnError:
        stopped = True
    return data, errors[KEY], stopped


class TestValidator:
    def test_empty_is_ignored(self):
        data, errors, stopped = validate("", fake_model())
        assert not errors and not stopped

    def test_view_of_this_dataset(self):
        model = fake_model([package()], [resource()], [view()])
        data, errors, stopped = validate("view-1", model)
        assert not errors and not stopped
        assert data[KEY] == "view-1"

    @pytest.mark.parametrize(
        "model",
        [
            # no such view
            fake_model([package()], [resource()], []),
            # view of another dataset's resource
            fake_model(
                [package(), package("pkg-2")],
                [resource("res-2", package_id="pkg-2")],
                [view(resource_id="res-2")],
            ),
            # view of a deleted resource
            fake_model([package()], [resource(state="deleted")], [view()]),
        ],
    )
    def test_rejects_other_views(self, model):
        data, errors, stopped = validate("view-1", model)
        assert stopped
        assert errors == ["Choose a view of one of this dataset's resources."]

    def test_new_dataset_cannot_have_one(self):
        # no id yet, so no views of its own
        model = fake_model([], [resource()], [view()])
        _, errors, stopped = validate("view-1", model, package_id=None)
        assert stopped and errors

    def test_stale_saved_value_is_dropped(self):
        # e.g. its resource was deleted: resource_delete re-saves the dataset
        # with the old value, and that must not fail
        model = fake_model(
            [package(**{FIELD_NAME: "view-1"})], [resource(state="deleted")], [view()]
        )
        data, errors, stopped = validate("view-1", model)
        assert stopped and not errors
        assert KEY not in data

    def test_new_invalid_value_is_rejected_even_with_one_saved(self):
        model = fake_model([package(**{FIELD_NAME: "view-1"})], [resource()], [view()])
        _, errors, stopped = validate("view-2", model)
        assert stopped and errors


@pytest.fixture
def actions(monkeypatch):
    """Fake actions. Fill in ``views`` (id -> dict) and ``packages`` (id -> dict);
    anything missing raises ObjectNotFound."""
    state = SimpleNamespace(views={}, packages={}, view_lists={}, unauthorized=set())

    def lookup(table, data_dict):
        key = data_dict["id"]
        if key in state.unauthorized:
            raise toolkit.NotAuthorized()
        if key not in table:
            raise toolkit.ObjectNotFound()
        return table[key]

    fakes = {
        "resource_view_show": lambda context, data_dict: lookup(state.views, data_dict),
        "package_show": lambda context, data_dict: lookup(state.packages, data_dict),
        "resource_view_list": lambda context, data_dict: state.view_lists.get(
            data_dict["id"], []
        ),
    }
    monkeypatch.setattr(canonical_view.toolkit, "get_action", lambda name: fakes[name])
    return state


class TestCanonicalViewHelper:
    def pkg(self, **fields):
        return dict({"id": "pkg-1", "resources": [{"id": "res-1", "name": "Data"}]}, **fields)

    def test_not_set(self, actions):
        assert wprdc_canonical_view(self.pkg()) is None

    def test_returns_view_and_resource(self, actions):
        actions.views["view-1"] = {"id": "view-1", "resource_id": "res-1", "title": "Map"}
        result = wprdc_canonical_view(self.pkg(**{FIELD_NAME: "view-1"}))
        assert result == {
            "resource_view": actions.views["view-1"],
            "resource": {"id": "res-1", "name": "Data"},
        }

    def test_deleted_view(self, actions):
        assert wprdc_canonical_view(self.pkg(**{FIELD_NAME: "gone"})) is None

    def test_view_not_visible(self, actions):
        actions.views["view-1"] = {"id": "view-1", "resource_id": "res-1"}
        actions.unauthorized.add("view-1")
        assert wprdc_canonical_view(self.pkg(**{FIELD_NAME: "view-1"})) is None

    def test_view_of_resource_not_in_dataset(self, actions):
        actions.views["view-1"] = {"id": "view-1", "resource_id": "elsewhere"}
        assert wprdc_canonical_view(self.pkg(**{FIELD_NAME: "view-1"})) is None


class TestOptionsHelper:
    def test_every_view_of_every_resource(self, actions):
        actions.packages["pkg-1"] = {
            "id": "pkg-1",
            "resources": [{"id": "res-1", "name": "GeoJSON"}, {"id": "res-2", "name": "Excel"}],
        }
        actions.view_lists = {
            "res-1": [{"id": "v1", "title": "Map"}, {"id": "v2", "title": "Table"}],
            "res-2": [{"id": "v3", "title": "Table"}],
        }
        assert wprdc_canonical_view_options("pkg-1") == [
            {"value": "v1", "text": "GeoJSON: Map"},
            {"value": "v2", "text": "GeoJSON: Table"},
            {"value": "v3", "text": "Excel: Table"},
        ]

    @pytest.mark.parametrize("package_id", [None, "", "missing"])
    def test_no_dataset(self, actions, package_id):
        assert wprdc_canonical_view_options(package_id) == []

    def test_dataset_not_visible(self, actions):
        actions.unauthorized.add("pkg-1")
        assert wprdc_canonical_view_options("pkg-1") == []

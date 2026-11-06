"""Canonical view: one resource view chosen to represent the whole dataset.

The view id is stored on the dataset as ``canonical_view_id`` (a scheming
field) and rendered on the dataset page between the description and the
resource list.
"""
from typing import Any, Optional

import ckan.plugins.toolkit as toolkit

FIELD_NAME = "canonical_view_id"


def _view_resource_in_package(model, view_id: str, package) -> bool:
    view = model.ResourceView.get(view_id)
    if not view:
        return False
    resource = model.Resource.get(view.resource_id)
    return bool(
        resource
        and resource.state == "active"
        and resource.package_id == package.id
    )


def canonical_view_validator(key, data, errors, context):
    """The view must belong to an active resource of this dataset.

    A value that was already saved but no longer points at a valid view (its
    view or resource was deleted) is dropped rather than rejected, so it can't
    block unrelated updates such as ``resource_delete``, which re-saves the
    whole dataset.
    """
    value = data.get(key)
    if not value:
        return

    model = context["model"]
    package_id = data.get(("id",))
    package = model.Package.get(package_id) if package_id else None
    if package and _view_resource_in_package(model, value, package):
        return

    saved = package.extras.get(FIELD_NAME) if package else None
    if value == saved:
        data.pop(key, None)
        raise toolkit.StopOnError

    errors[key].append(toolkit._("Choose a view of one of this dataset's resources."))
    raise toolkit.StopOnError


def wprdc_canonical_view(pkg: dict) -> Optional[dict[str, Any]]:
    """The dataset's canonical view and its resource, or None.

    Returns None if none is set, or if the view is gone or not visible to the
    current user.
    """
    view_id = pkg.get(FIELD_NAME)
    if not view_id:
        return None
    try:
        view = toolkit.get_action("resource_view_show")({}, {"id": view_id})
    except (toolkit.ObjectNotFound, toolkit.NotAuthorized):
        return None
    resource = next(
        (r for r in pkg.get("resources") or [] if r["id"] == view["resource_id"]),
        None,
    )
    if not resource:
        return None
    return {"resource_view": view, "resource": resource}


def wprdc_canonical_view_options(package_id: Optional[str]) -> list[dict[str, str]]:
    """Options for the canonical-view select: every view of every resource.

    Each option is ``{"value": view id, "text": "Resource name: View title"}``.
    Empty for a dataset that doesn't exist yet.
    """
    if not package_id:
        return []
    try:
        pkg = toolkit.get_action("package_show")({}, {"id": package_id})
    except (toolkit.ObjectNotFound, toolkit.NotAuthorized):
        return []

    options = []
    for resource in pkg.get("resources") or []:
        views = toolkit.get_action("resource_view_list")({}, {"id": resource["id"]})
        resource_name = toolkit.h.resource_display_name(resource)
        for view in views:
            options.append(
                {"value": view["id"], "text": f"{resource_name}: {view['title']}"}
            )
    return options

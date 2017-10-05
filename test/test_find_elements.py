import pytest
from unittest.mock import Mock


def test__custom_view_class__elements_wrapped(view, custom_view_cls):
    elements = view.find_elements("", "", view_cls=custom_view_cls)
    assert all([isinstance(e, custom_view_cls.__class__) for e in elements]), "Elements not wrapped custom view class"


def test__custom_view_class__subclass__doesnt_raise_error(view, custom_view_cls):
    try:
        view.find_elements("", "", custom_view_cls)
    except ValueError:
        pytest.fail(f"Error thrown with a subclass of View")


def test__custom_view_class__non_subclass__raises_error(view):
    try:
        view.find_elements("", "", Mock())
    except ValueError:
        pass
    else:
        pytest.fail(f"Error not thrown with a non subclass of View")

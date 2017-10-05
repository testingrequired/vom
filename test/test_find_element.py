import pytest
from unittest.mock import Mock


def test__custom_view_class__element_wrapped(view, custom_view_cls):
    element = view.find_element("", "", view_cls=custom_view_cls)
    assert isinstance(element, custom_view_cls.__class__), "Element not wrapped custom view class"


def test__custom_view_class__subclass__doesnt_raise_error(view, custom_view_cls):
    try:
        view.find_element("", "", view_cls=custom_view_cls)
    except ValueError:
        pytest.fail(f"Error thrown with a subclass of View")


def test__custom_view_class__non_subclass__raises_error(view):
    try:
        view.find_element("", "", view_cls=Mock())
    except ValueError:
        pass
    else:
        pytest.fail(f"Error not thrown with a non subclass of View")

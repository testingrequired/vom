import pytest
from unittest.mock import Mock


def test__custom_view_class__element_wrapped(view, custom_view_cls):
    element = view.find_element("", "", view_cls=custom_view_cls)
    assert isinstance(element, custom_view_cls.__class__), "Element not wrapped custom view class"

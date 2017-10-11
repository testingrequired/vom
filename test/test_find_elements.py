import pytest
from unittest.mock import Mock
from selenium.webdriver.remote.webdriver import WebElement


def test__find_elements_by_text__custom_selector(view):
    view.find_elements_by_css_selector = Mock()
    view.find_elements_by_css_selector.return_value = [Mock(spec=WebElement)]
    view.find_elements_by_text("", selector="p")
    view.find_elements_by_css_selector.assert_called_once_with("p", None)


def test__custom_view_class__elements_wrapped(view, custom_view_cls):
    elements = view.find_elements("", "", view_cls=custom_view_cls)
    assert all([isinstance(e, custom_view_cls.__class__) for e in elements]), "Elements not wrapped custom view class"

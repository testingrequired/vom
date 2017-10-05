import pytest
from vom import View
from unittest.mock import Mock
from selenium.webdriver.remote.webdriver import WebElement


def test__custom_view_class__subclass__doesnt_raise_error(element):
    view = View(lambda: element)

    try:
        view.find_element("", "", Mock(spec=View))
    except ValueError:
        pytest.fail(f"Error thrown with a subclass of View")


def test__custom_view_class__non_subclass__raises_error(element):
    view = View(lambda: element)

    try:
        view.find_element("", "", Mock())
    except ValueError:
        pass
    else:
        pytest.fail(f"Error not thrown with a non subclass of View")

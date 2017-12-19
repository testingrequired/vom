import pytest
from mock import Mock
from selenium.webdriver.remote.webdriver import WebElement


def test__find_elements_by_text__custom_selector(view):
    view.find_elements_by_css_selector = Mock()
    view.find_elements_by_css_selector.return_value = [Mock(spec=WebElement)]
    view.find_elements_by_text("", selector="p")
    view.find_elements_by_css_selector.assert_called_once_with("p", None)

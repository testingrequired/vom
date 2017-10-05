import pytest
from unittest.mock import Mock
from selenium.webdriver.remote.webdriver import WebElement


@pytest.fixture(scope="function")
def element():
    e = Mock(spec=WebElement)
    e.find_element = Mock()
    e.find_element.return_value = Mock(spec=WebElement)
    e.find_elements = Mock()
    e.find_elements.return_value = []
    return e
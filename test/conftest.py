import pytest
from mock import Mock
from selenium.webdriver.remote.webdriver import WebElement
from vom import View


@pytest.fixture(scope="function")
def element():
    e = Mock(spec=WebElement)
    e.find_element = Mock()
    e.find_element.return_value = Mock(spec=WebElement)
    e.find_elements = Mock()
    e.find_elements.return_value = [
        Mock(spec=WebElement), Mock(spec=WebElement)]
    return e


@pytest.fixture(scope="function")
def view(element):
    return View(lambda: element)


@pytest.fixture(scope="function")
def custom_view_cls():
    return Mock(spec=View)

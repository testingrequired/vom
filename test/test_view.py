import pytest
from vom import View
from mock import Mock
from selenium.webdriver.remote.webdriver import WebElement


@pytest.fixture
def element():
    return Mock(spec=WebElement)


def test__view(element):
    try:
        View(lambda: element)
    except Exception as e:
        pytest.fail("Failed to initialize View: {}".format(e))

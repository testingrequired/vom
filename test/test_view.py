import pytest
from vom import View
from unittest.mock import Mock
from selenium.webdriver.remote.webdriver import WebElement


@pytest.fixture
def element():
    return Mock(spec=WebElement)


def test__view(element: WebElement):
    try:
        View(lambda: element)
    except Exception as e:
        pytest.fail(f"Failed to initialize View: {e}")

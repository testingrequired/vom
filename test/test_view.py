import pytest
from vom import View


def test__view(element):
    try:
        View(lambda: element)
    except Exception as e:
        pytest.fail("Failed to initialize View: {}".format(e))

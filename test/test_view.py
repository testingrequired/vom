import pytest
from vom import View

def test__view():
    try:
        View(lambda: None)
    except Exception as e:
        pytest.fail(f"Failed to initialize View: {e}")
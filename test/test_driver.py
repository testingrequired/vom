import pytest
from unittest.mock import Mock
from selenium.common.exceptions import NoSuchElementException


def test__driver__root_element__not_displayed_raises_error(view):
    view.root = Mock(side_effect=NoSuchElementException())

    try:
        view.driver
    except RuntimeError:
        pass
    else:
        pytest.fail(f"No exception raised")

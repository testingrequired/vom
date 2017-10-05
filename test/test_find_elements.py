import pytest
from vom import View
from unittest.mock import Mock


def test__custom_view_class__subclass__doesnt_raise_error(element):
    view = View(lambda: element)
    subclass = Mock(spec=View)

    try:
        view.find_elements("", "", subclass)
    except ValueError:
        pytest.fail(f"Error thrown with a subclass of View")


def test__custom_view_class__non_subclass__raises_error(element):
    view = View(lambda: element)

    try:
        view.find_elements("", "", Mock())
    except ValueError:
        pass
    else:
        pytest.fail(f"Error not thrown with a non subclass of View")

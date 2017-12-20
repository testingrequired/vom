import pytest
from mock import Mock, PropertyMock
from vom import View


def test__view(element):
    try:
        View(lambda: element)
    except Exception as e:
        pytest.fail("Failed to initialize View: {}".format(e))


def test__id__calls_id_on_root(element, view):
    element.id = PropertyMock()
    _ = view.id
    element.id.assert_called()


def test__get_attribute__calls_on_root(element, view):
    element.get_attribute = Mock()
    value = "foobar"
    _ = view.get_attribute(value)
    element.get_attribute.assert_called_with(value)


def test__get_property__calls_on_root(element, view):
    element.get_property = Mock()
    value = "foobar"
    _ = view.get_property(value)
    element.get_property.assert_called_with(value)


def test__tag_name__calls_on_root(element, view):
    element.tag_name = PropertyMock()
    _ = view.tag_name
    element.tag_name.assert_called()


def test__text__calls_on_root(element, view):
    element.text = PropertyMock()
    _ = view.text
    element.text.assert_called()


def test__rect__calls_on_root(element, view):
    element.rect = PropertyMock()
    _ = view.rect
    element.rect.assert_called()


def test__size__calls_on_root(element, view):
    element.size = PropertyMock()
    _ = view.size
    element.size.assert_called()


def test__location__calls_on_root(element, view):
    element.location = PropertyMock()
    _ = view.location
    element.location.assert_called()


def test__location_once_scrolled_into_view__calls_on_root(element, view):
    element.location_once_scrolled_into_view = PropertyMock()
    _ = view.location_once_scrolled_into_view
    element.location_once_scrolled_into_view.assert_called()


def test__is_enabled__calls_on_root(element, view):
    element.is_enabled = PropertyMock()
    _ = view.is_enabled
    element.is_enabled.assert_called()


def test__is_selected__calls_on_root(element, view):
    element.is_selected = PropertyMock()
    _ = view.is_selected
    element.is_selected.assert_called()


def test__is_displayed__calls_on_root(element, view):
    element.is_displayed = PropertyMock()
    _ = view.is_displayed
    element.is_displayed.assert_called()


def test__value_of_css_property__calls_on_root(element, view):
    element.value_of_css_property = Mock()
    value = "foobar"
    _ = view.value_of_css_property(value)
    element.value_of_css_property.assert_called_with(value)


def test__click__calls_on_root(element, view):
    element.click = Mock()
    _ = view.click()
    element.click.assert_called()


def test__clear__calls_on_root(element, view):
    element.clear = Mock()
    _ = view.clear()
    element.clear.assert_called()


def test__send_keys__calls_on_root(element, view):
    element.send_keys = Mock()
    value = "foobar"
    _ = view.send_keys(value)
    element.send_keys.assert_called_with(value)


def test__submit__calls_on_root(element, view):
    element.submit = Mock()
    _ = view.submit()
    element.submit.assert_called()

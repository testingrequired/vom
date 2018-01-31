from typing import Union, Callable, List, Any
from selenium.webdriver.remote.webdriver import WebDriver, WebElement, By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import NoSuchElementException
from future.utils import raise_from


class View(object):
    """
    Base View
    """

    def __init__(self, target, parent=None):
        # type: (Union[WebDriver, Callable[[], WebElement]], View) -> None
        """
        View accepts either a WebDriver instance or a callable returning a WebElement

        Usage::

            def get_example_form():
                return driver.find_element_by_id("exampleForm")

            view = View(driver)
            view.root = get_example_form

            # or

            view = View(get_example_form)
        """

        self._root = lambda: None  # type: Callable[[], WebElement]
        self._driver = None  # type: Union[Callable[[], WebDriver], None]
        self.parent = parent  # type: View

        if isinstance(target, WebDriver):
            self._init_from_driver(target)

        if isinstance(target, Callable):
            self._init_from_callable(target)

    def __str__(self):
        return self.text

    def __getattr__(self, item):
        try:
            return getattr(self.root, item)
        except AttributeError as e:
            raise_from(AttributeError("Neither View or root WebElement has method `{}`".format(item)), e)

    @property
    def root(self):
        # type: () -> WebElement
        element = self._root()  # type: WebElement
        return element

    @root.setter
    def root(self, value):
        # type: (WebElement) -> None
        self._root = value

    @property
    def driver(self):
        # type: () -> WebDriver
        try:
            d = self._driver()
        except NoSuchElementException as e:
            raise_from(RuntimeError("Root element not present on the page"), e)
        else:
            return d

    @driver.setter
    def driver(self, value):
        # type: (WebDriver) -> None
        self._driver = value

    def _init_from_driver(self, driver):
        # type: (WebDriver) -> None
        self.driver = lambda: driver
        self.root = lambda: self.driver.find_element_by_tag_name("html")

    def _init_from_callable(self, root):
        # type: (Callable[[], WebElement]) -> None
        self.root = root
        self.driver = lambda: self.root.parent

    def __eq__(self, other):
        # type: (View) -> bool
        return self.id == other.id

    # Properties

    @property
    def title(self):
        # type: () -> str
        return self.root.get_attribute("title")

    # Transform

    @property
    def as_select(self):
        # type: () -> Select
        return Select(self.root)

    # Content

    @property
    def inner_html(self):
        # type: () -> str
        return self.root.get_attribute("innerHTML")

    @property
    def outer_html(self):
        # type: () -> str
        return self.root.get_attribute("outerHTML")

    @property
    def inner_text(self):
        # type: () -> str
        return self.root.get_attribute("innerText")

    # State

    @property
    def is_enabled(self):
        # type: () -> bool
        return self.root.is_enabled()

    @property
    def is_selected(self):
        # type: () -> bool
        return self.root.is_selected()

    @property
    def is_displayed(self):
        # type: () -> bool
        result = False
        try:
            result = self.root.is_displayed()
        except NoSuchElementException:
            pass
        finally:
            return result

    def has_class(self, value):
        # type: (str) -> bool
        classes = self.get_attribute("class").split(" ")
        return value in classes

    # Javascript

    def execute_script(self, script, *args):
        # type: (str, *Any) -> Any
        return self.driver.execute_script(script, *([self.root] + list(args)))

    def execute_async_script(self, script, *args):
        # type: (str, *Any) -> Any
        return self.driver.execute_async_script(script, *args)

    # Actions

    def send_keys(self, value, clear=False):
        # type: (str, bool) -> None
        if clear:
            self.clear()
        self.root.send_keys(value)

    def focus(self):
        # type: () -> None
        self.execute_script("arguments[0].focus()")

    def blur(self):
        # type: () -> None
        self.execute_script("arguments[1].blur()")

    # Find Element/s

    def find_element(self, by, value, view_cls=None):
        # type: (By, Any, View) -> View
        """
        Find one element matching condition
        :param by: Type of condition
        :param value: Condition value
        :param view_cls: Optional custom class to wrap returned elements
        :return: Matching element wrapped in a view
        """
        if view_cls is None:
            view_cls = View

        return view_cls(lambda: self.root.find_element(by, value), self)

    def find_elements(self, by, value, view_cls=None):
        # type: (By, Any, Value) -> List[View]
        """
        Find one or more elements matching condition
        :param by: Type of condition
        :param value: Condition value
        :param view_cls: Optional custom class to wrap returned elements
        :return: List of matching web elements wrapped in a view
        """
        if view_cls is None:
            view_cls = View

        def get_elements():
            results = []

            try:
                results = self.root.find_elements(by, value)
            except NoSuchElementException:
                pass
            finally:
                return results

        def get_element_at_index(i):
            return lambda: get_elements()[i]

        return [view_cls(get_element_at_index(i), self) for i, element in enumerate(get_elements())]

    def find_element_by_css_selector(self, value, view_cls=None):
        # type: (str, View) -> View
        return self.find_element(By.CSS_SELECTOR, value, view_cls)

    def find_elements_by_css_selector(self, value, view_cls=None):
        # type: (str, View) -> List[View]
        return self.find_elements(By.CSS_SELECTOR, value, view_cls)

    def find_element_by_tag_name(self, value, view_cls=None):
        # type: (str, View) -> View
        return self.find_element(By.TAG_NAME, value, view_cls)

    def find_elements_by_tag_name(self, value, view_cls=None):
        # type: (str, View) -> List[View]
        return self.find_elements(By.TAG_NAME, value, view_cls)

    def find_element_by_xpath(self, value, view_cls=None):
        # type: (str, View) -> View
        return self.find_element(By.XPATH, value, view_cls)

    def find_elements_by_xpath(self, value, view_cls=None):
        # type: (str, View) -> List[View]
        return self.find_elements(By.XPATH, value, view_cls)

    def find_element_by_class_name(self, value, view_cls=None):
        # type: (str, View) -> View
        return self.find_element(By.CLASS_NAME, value, view_cls)

    def find_elements_by_class_name(self, value, view_cls=None):
        # type: (str, View) -> List[View]
        return self.find_elements(By.CLASS_NAME, value, view_cls)

    def find_element_by_id(self, value, view_cls=None):
        # type: (str, View) -> View
        return self.find_element(By.ID, value, view_cls)

    def find_elements_by_id(self, value, view_cls=None):
        # type: (str, View) -> List[View]
        return self.find_elements(By.ID, value, view_cls)

    def find_element_by_link_text(self, value, view_cls=None):
        # type: (str, View) -> View
        return self.find_element(By.LINK_TEXT, value, view_cls)

    def find_elements_by_link_text(self, value, view_cls=None):
        # type: (str, View) -> List[View]
        return self.find_elements(By.LINK_TEXT, value, view_cls)

    def find_element_by_partial_link_text(self, value, view_cls=None):
        # type: (str, View) -> View
        return self.find_element(By.PARTIAL_LINK_TEXT, value, view_cls)

    def find_elements_by_partial_link_text(self, value, view_cls=None):
        # type: (str, View) -> List[View]
        return self.find_elements(By.PARTIAL_LINK_TEXT, value, view_cls)

    def find_element_by_name(self, value, view_cls=None):
        # type: (str, View) -> View
        return self.find_element(By.NAME, value, view_cls)

    def find_elements_by_name(self, value, view_cls=None):
        # type: (str, View) -> List[View]
        return self.find_elements(By.NAME, value, view_cls)

    def find_elements_by_text(self, value, selector="*", view_cls=None):
        # type: (str, str, View) -> List[View]
        return [e for e in self.find_elements_by_css_selector(selector, view_cls) if e.text == value]

    def find_element_by_text(self, value, selector="*", view_cls=None):
        # type: (str, str, View) -> View
        elements = self.find_elements_by_text(value, selector, view_cls)
        if len(elements) == 0:
            raise NoSuchElementException(
                "No elements found with text: `{}`".format(value))
        return elements[0]

    def find_elements_by_partial_text(self, value, selector="*", view_cls=None):
        # type: (str, str, View) -> List[View]
        return [e for e in self.find_elements_by_css_selector(selector, view_cls) if value in e.text]

    def find_element_by_partial_text(self, value, selector="*", view_cls=None):
        # type: (str, str, View) -> View
        elements = self.find_elements_by_partial_text(
            value, selector, view_cls)
        if len(elements) == 0:
            raise NoSuchElementException(
                "No elements found with text: `{}`".format(value))
        return elements[0]

    def find_inputs_by_placeholder(self, value, view_cls=None):
        # type: (str, View) -> List[View]
        return self.find_elements_by_css_selector("input[type=text][placeholder='{}']".format(value), view_cls)

    def find_input_by_placeholder(self, value, view_cls=None):
        # type: (str, View) -> View
        return self.find_element_by_css_selector("input[placeholder='{}']".format(value), view_cls)

    # Waiting

    def wait_until_displayed(self, timeout=10):
        # type: (int) -> None
        return WebDriverWait(None, timeout).until(lambda _: self.is_displayed)

    def wait_until_not_displayed(self, timeout=10):
        # type: (int) -> None
        return WebDriverWait(None, timeout).until(lambda _: not self.is_displayed)

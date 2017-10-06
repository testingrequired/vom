from typing import Union, Callable, List
from selenium.webdriver.remote.webdriver import WebDriver, WebElement, By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import NoSuchElementException


class View(object):
    """
    Base View
    """

    def __init__(self, target: Union[WebDriver, Callable[[], WebElement]], parent: "View" = None):
        """
        View accepts either a WebDriver instance or a callable returning a WebElement

        Usage::

            def get_example_form():
                return driver.find_element_by_id("exampleForm")

            view = View(driver)
            view.root = get_example_form

            # or

            view = View(get_example_form)

        :param Union[WebDriver, Callable[[], WebElement] target:
        """
        self._root: Union[Callable[[], WebElement], Callable[[], None]] = lambda: None
        self._driver: Union[Callable[[], WebDriver], None] = None
        self.parent = parent

        if isinstance(target, WebDriver):
            self._init_from_driver(target)

        if isinstance(target, Callable):
            self._init_from_callable(target)

    def __str__(self):
        return self.text

    @property
    def root(self) -> WebElement:
        return self._root()

    @root.setter
    def root(self, value):
        self._root = value

    @property
    def driver(self):
        try:
            d = self._driver()
        except NoSuchElementException as e:
            raise RuntimeError(f"Root element not present on the page") from e
        else:
            return d

    @driver.setter
    def driver(self, value):
        self._driver = value

    def _init_from_driver(self, driver: WebDriver):
        self.driver: WebDriver = lambda: driver
        self.root = lambda: self.driver.find_element_by_tag_name("html")

    def _init_from_callable(self, root: Callable[[], WebElement]):
        self.root = root
        self.driver: Callable[[], WebDriver] = lambda: self.root.parent

    def __eq__(self, other: "View"):
        return self.id == other.id

    @property
    def id(self):
        return self.root.id

    # Properties

    def get_attribute(self, name):
        self.root.get_attribute(name)

    def get_property(self, name):
        return self.root.get_property(name)

    @property
    def title(self):
        return self.execute_script("return arguments[0].title")

    @property
    def tag_name(self):
        return self.root.tag_name

    @property
    def text(self):
        return self.root.text

    # Transform

    @property
    def as_select(self):
        return Select(self.root)

    ## Content

    @property
    def inner_html(self):
        return self.root.get_attribute("innerHTML")

    @property
    def outer_html(self):
        return self.root.get_attribute("outerHTML")

    @property
    def inner_text(self):
        return self.root.get_attribute("innerText")

    ## Dimensions/Location

    @property
    def rect(self):
        return self.root.rect

    @property
    def size(self):
        return self.root.size

    @property
    def location(self):
        return self.root.location

    @property
    def location_once_scrolled_into_view(self):
        return self.root.location_once_scrolled_into_view

    ## State

    @property
    def is_enabled(self):
        return self.root.is_enabled()

    @property
    def is_selected(self):
        return self.root.is_selected()

    @property
    def is_displayed(self):
        return self.root.is_displayed()

    def has_class(self, value):
        classes = self.get_attribute("class").split(" ")
        return value in classes

    ## Style/CSS

    def value_of_css_property(self, property_name):
        return self.root.value_of_css_property(property_name)

    # Javascript

    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *[self.root, *args])

    def execute_async_script(self, script, *args):
        return self.driver.execute_async_script(script, *args)

    # Actions

    def click(self):
        self.root.click()

    def clear(self):
        self.root.clear()

    def send_keys(self, value, clear: bool = False):
        if clear:
            self.clear()
        self.root.send_keys(value)

    def submit(self):
        self.root.submit()

    def focus(self):
        self.execute_script("arguments[0].focus()")

    def blur(self):
        self.execute_script("arguments[1].blur()")

    # Find Element/s

    def find_element(self, by: By, value, view_cls: "View" = None) -> "View":
        """
        Find one element matching condition
        :param by: Type of condition
        :param value: Condition value
        :param cls: Optional custom class to wrap returned elements
        :return: Matching element wrapped in a view
        """
        if view_cls is not None and not issubclass(view_cls.__class__, View):
            raise ValueError(f"cls must be a subclass of View")
        else:
            view_cls = View

        return view_cls(lambda: self.root.find_element(by, value), self)

    def find_elements(self, by: By, value, view_cls: "View" = None) -> List["View"]:
        """
        Find one or more elements matching condition
        :param by: Type of condition
        :param value: Condition value
        :param cls: Optional custom class to wrap returned elements
        :return: List of matching web elements wrapped in a view
        """
        if view_cls is not None and not issubclass(view_cls.__class__, View):
            raise ValueError(f"cls must be a subclass of View")
        else:
            view_cls = View

        def get_elements():
            return self.root.find_elements(by, value)

        def get_element_at_index(i):
            return lambda: get_elements()[i]

        return [view_cls(get_element_at_index(i), self) for i, element in enumerate(get_elements())]

    def find_element_by_css_selector(self, value, view_cls = None):
        return self.find_element(By.CSS_SELECTOR, value, view_cls)

    def find_elements_by_css_selector(self, value, view_cls = None):
        return self.find_elements(By.CSS_SELECTOR, value, view_cls)

    def find_element_by_tag_name(self, value, view_cls = None):
        return self.find_element(By.TAG_NAME, value, view_cls)

    def find_elements_by_tag_name(self, value, view_cls = None):
        return self.find_elements(By.TAG_NAME, value, view_cls)

    def find_element_by_xpath(self, value, view_cls = None):
        return self.find_element(By.XPATH, value, view_cls)

    def find_elements_by_xpath(self, value, view_cls = None):
        return self.find_elements(By.XPATH, value, view_cls)

    def find_element_by_class_name(self, value, view_cls = None):
        return self.find_element(By.CLASS_NAME, value, view_cls)

    def find_elements_by_class_name(self, value, view_cls = None):
        return self.find_elements(By.CLASS_NAME, value, view_cls)

    def find_element_by_id(self, value, view_cls = None):
        return self.find_element(By.ID, value, view_cls)

    def find_elements_by_id(self, value, view_cls = None):
        return self.find_elements(By.ID, value, view_cls)

    def find_element_by_link_text(self, value, view_cls = None):
        return self.find_element(By.LINK_TEXT, value, view_cls)

    def find_elements_by_link_text(self, value, view_cls = None):
        return self.find_elements(By.LINK_TEXT, value, view_cls)

    def find_element_by_partial_link_text(self, value, view_cls = None):
        return self.find_element(By.PARTIAL_LINK_TEXT, value, view_cls)

    def find_elements_by_partial_link_text(self, value, view_cls = None):
        return self.find_elements(By.PARTIAL_LINK_TEXT, value, view_cls)

    def find_element_by_name(self, value, view_cls = None):
        return self.find_element(By.NAME, value, view_cls)

    def find_elements_by_name(self, value, view_cls = None):
        return self.find_elements(By.NAME, value, view_cls)

    def find_elements_by_text(self, value, selector="*", view_cls = None):
        return [e for e in self.find_elements_by_css_selector(selector, view_cls) if e.text == value]

    def find_element_by_text(self, value, selector="*", view_cls = None):
        elements = self.find_elements_by_text(value, selector, view_cls)
        if len(elements) == 0:
            raise NoSuchElementException(f"No elements found with text: `{value}`")
        return elements[0]

    def find_elements_by_partial_text(self, value, selector="*", view_cls = None):
        return [e for e in self.find_elements_by_css_selector(selector, view_cls) if value in e.text]

    def find_element_by_partial_text(self, value, selector="*", view_cls = None):
        elements = self.find_elements_by_partial_text(value, selector, view_cls)
        if len(elements) == 0:
            raise NoSuchElementException(f"No elements found with text: `{value}`")
        return elements[0]

    def find_inputs_by_placeholder(self, value, view_cls=None):
        return self.find_elements_by_css_selector(f"input[type=text][placeholder='{value}']", view_cls)

    def find_input_by_placeholder(self, value, view_cls=None):
        return self.find_element_by_css_selector(f"input[placeholder='{value}']", view_cls)


    # Waiting

    def wait_until_displayed(self, timeout=10):
        return WebDriverWait(None, timeout).until(lambda _: self.is_displayed)

    def wait_until_not_displayed(self, timeout=10):
        return WebDriverWait(None, timeout).until(lambda _: not self.is_displayed)

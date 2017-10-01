from typing import Union, Callable, List
from selenium.webdriver.remote.webdriver import WebDriver, WebElement, By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import NoSuchElementException


class View(object):
    """
    Base View
    """

    def __init__(self, target: Union[WebDriver, Callable], parent: "View" = None):
        """
        View accepts either a WebDriver instance or a callable returning a WebElement

        Usage::

            def get_example_form():
                return driver.find_element_by_id("exampleForm")

            view = View(driver)
            view.set_root_element(get_example_form)

            # or

            view = View(get_example_form)
        :param Union[WebDriver,Callable] target:
        """
        self._root: Union[Callable[[], WebElement], Callable[[], None]] = lambda: None
        self.driver: Union[WebDriver, None] = None
        self.parent = parent

        if isinstance(target, WebDriver):
            self._init_from_driver(target)

        if isinstance(target, Callable):
            self._init_from_callable(target)

        print()

    @property
    def root(self) -> WebElement:
        return self._root()

    @root.setter
    def root(self, value):
        self._root = value

    def _init_from_driver(self, driver: WebDriver):
        self.driver: WebDriver = driver
        self.root = lambda: self.driver.find_element_by_tag_name("html")
        print()

    def _init_from_callable(self, fn: Callable[[], WebDriver]):
        element = fn()

        if not isinstance(element, WebElement):
            raise ValueError(f"target must be a callable returning a WebElement")

        self.root = fn
        self.driver: WebDriver = element.parent

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

    def find_element(self, by: By, value) -> "View":
        return View(lambda: self.root.find_element(by, value), self)

    def find_elements(self, by: By, value) -> List["View"]:
        def get_elements():
            return self.root.find_elements(by, value)

        def get_element_at_index(i):
            return lambda: get_elements()[i]

        return [View(get_element_at_index(i), self) for i, element in enumerate(get_elements())]

    def find_element_by_css_selector(self, value):
        return self.find_element(By.CSS_SELECTOR, value)

    def find_elements_by_css_selector(self, value):
        return self.find_elements(By.CSS_SELECTOR, value)

    def find_element_by_tag_name(self, value):
        return self.find_element(By.TAG_NAME, value)

    def find_elements_by_tag_name(self, value):
        return self.find_elements(By.TAG_NAME, value)

    def find_element_by_xpath(self, value):
        return self.find_element(By.XPATH, value)

    def find_elements_by_xpath(self, value):
        return self.find_elements(By.XPATH, value)

    def find_element_by_class_name(self, value):
        return self.find_element(By.CLASS_NAME, value)

    def find_elements_by_class_name(self, value):
        return self.find_elements(By.CLASS_NAME, value)

    def find_element_by_id(self, value):
        return self.find_element(By.ID, value)

    def find_elements_by_id(self, value):
        return self.find_elements(By.ID, value)

    def find_element_by_link_text(self, value):
        return self.find_element(By.LINK_TEXT, value)

    def find_elements_by_link_text(self, value):
        return self.find_elements(By.LINK_TEXT, value)

    def find_element_by_partial_link_text(self, value):
        return self.find_element(By.PARTIAL_LINK_TEXT, value)

    def find_elements_by_partial_link_text(self, value):
        return self.find_elements(By.PARTIAL_LINK_TEXT, value)

    def find_element_by_name(self, value):
        return self.find_element(By.NAME, value)

    def find_elements_by_name(self, value):
        return self.find_elements(By.NAME, value)

    def find_elements_by_text(self, value):
        return [e for e in self.find_elements_by_css_selector("*") if e.text == value]

    def find_element_by_text(self, value):
        elements = self.find_elements_by_text(value)
        if len(elements) == 0:
            raise NoSuchElementException(f"No elements found with text: `{value}`")
        return elements[0]

    def find_elements_by_partial_text(self, value, selector="*"):
        return [e for e in self.find_elements_by_css_selector("*") if value in e.text]

    def find_element_by_partial_text(self, value):
        elements = self.find_elements_by_partial_text(value)
        if len(elements) == 0:
            raise NoSuchElementException(f"No elements found with text: `{value}`")
        return elements[0]


    # Waiting

    def wait_until_displayed(self, timeout=10):
        return WebDriverWait(self.driver, timeout).until(lambda d: self.is_displayed)

    def wait_until_not_displayed(self, timeout=10):
        return WebDriverWait(self.driver, timeout).until(lambda d: not self.is_displayed)
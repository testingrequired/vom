[![Build Status](https://travis-ci.org/testingrequired/vom.svg?branch=master)](https://travis-ci.org/testingrequired/vom)
[![PyPI version](https://badge.fury.io/py/vom.svg)](https://badge.fury.io/py/vom)

# vom

`vom` (View Object Model) is an opinionated framework for writing page objects for selenium tests/scripts

## Installation

Tested on Python 2.7.x & 3.6.x

```bash
$ pip install vom
```

## Usage

Defining view objects is as easy as extending `View`:

```python
from vom import View

class LoginForm(View):
    @property
    def username(self):
        return self.find_element_by_id("username")
    
    @property
    def password(self):
        return self.find_element_by_id("password")
    
    @property
    def submit_button(self):
        return self.find_element_by_css_selector("input[type='submit']")
```

Notice you don't see any references to a `WebDriver` instance. Lets initialize the view object:

```python
login = LoginForm(lambda: driver.find_element_by_id("login-form"))
```

The view object is initialized by passing a `Callable[[], WebElement]`. The `WebDriver` instance is object from the `WebElement`. Its a `Callable` because we need to be able to get a fresh reference to the `WebElement` at any time.

## Defining element properties

The view object `WebElement` references are should be defined as properties. This ensure fresh references to all elements. See [StaleElementReferenceException](http://selenium-python.readthedocs.io/api.html#selenium.common.exceptions.StaleElementReferenceException)

### Querying

All `find_element/s` methods on `WebElement` can be called on `View`. Results from these method calls will be wrapped in a `View`. Custom `View` implementations can be passed allowing for custom logic:

```python
from vom import View

class OptionComponent(View):
    @property
    def switch(self):
        self.driver.find_element_by_id("switch")
    
    def toggle(self):
        self.switch.click()

class SearchForm(View):
    @property
    def some_search_option(self):
        self.find_element_by_id("some-search-option-id", OptionComponent)

search = SearchForm(lambda: driver.find_element_by_id("search-form"))
search.some_search_option.toggle()
```

## `WebElement` API

`View` will proxy undefined method calls to its `WebElement` allowing you to treat them as a souped up `WebElement`.

## Utility Methods

There are a number of utility methods to supplement the `WebElement` methods.

### Find Element/s by Text

Similar to `find_element/s_by_link_text` & `find_element/s_by_partial_link_text` but across all tags. They also allow for a custom `selector`.

* `find_elements_by_text(value, selector="*")`
* `find_element_by_text(value, selector="*")`
* `find_elements_by_partial_text(value, selector="*")`
* `find_element_by_partial_text(value, selector="*")`

### Find Input/s

* `find_inputs_by_placeholder(value)`
* `find_input_by_placeholder(value)`

### Properties

* `title` Return the `WebElement` title property
* `has_class(value)` Returns if `WebElement` has css class

### Content

* `inner_html` Returns the `innerHTML` of the `WebElement`
* `outer_html` Returns the `outerHTML` of the `WebElement`
* `inner_text` Returns the `innerText` of the `WebElement`

### Waiting

* `wait_until_displayed(timeout=10)`
* `wait_until_not_displayed(timeout=10)`

### Actions

* `focus()` Focus the `WebElement`
* `blur()` Blur the `WebElement`

### Execute Script

Similar to `driver.execute_script` but `arguments[0]` is a reference to the `root` element of the `View`.

* `execute_script(script, *args)`
* `execute_async_script(script, *args)`

### Transform

* `as_select` Return the `WebElement` wrapped in a `Select`

## ViewDriver

`ViewDriver` is a utility class which wraps `WebDriver`. It provides similar `find_element/s` methods that `View` does.

```python
from selenium import webdriver
from vom import ViewDriver

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = ViewDriver(webdriver.Chrome(chrome_options=options))

    driver.get("http://example.com")

    login = driver.find_element_by_id("login-form", LoginForm)
    login.username.send_keys("")
    login.password.send_keys("")
    login.submit_buttom.click()
```
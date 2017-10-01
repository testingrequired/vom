# vom

`vom` (View Object Modal) is a library for writing page objects for selenium tests/scripts

## View Object vs Page Object

The term "page" is outdated in the context of modern web applications. The term "view" more aligned with the usage of self contained components (e.g. React, Angular, Vue). They represent the same concept however.

## Installation

```bash
$ pip install vom
```

## Getting Started

```python
from vom import View

class Login(View):
    @property
    def username(self):
        return self.find_element_by_name("username")
    
    @property
    def password(self):
        return self.find_element_by_name("password")
    
    @property
    def login_button(self):
        return self.find_element_by_id("loginBtn")
```

Then using:

```python
login = Login(lambda: driver.find_element_by_id("loginForm"))
```

or

```python
login = View(driver)
login.root = lambda: driver.find_element_by_id("loginForm")
```

### Element Properties

Elements should be properties on the `View` to ensure they never throw a `StaleElementReference`. These element properties are a `View` themselves all the way down.

## Root Element

The `root` element of the `View` is the underlying `WebElement`.

### Setting

The `root` can be set by assigning a `Callable[[], WebElement]`.

```python
login.root = lambda: driver.find_element_by_id("loginForm")
```

## Parent View

The `parent` is a reference to its parent `View`. Element properties `parent` will be the `View` that defined them.

## API

`View` mirrors much of the `WebElement` API with additional utility methods. The `find_element`/`find_elements` family of methods all return `View` instead of `WebElement` scoped within the `root` `WebElement`.

### Waiting

`View` has two methods to handle waiting for elements to appear or disappear (e.g. loading screens, async data loading).

```python
login.username.wait_until_displayed()
login.username.send_keys("")
login.password.send_keys("")
login.login_button.click()
login.wait_until_not_displayed()
```
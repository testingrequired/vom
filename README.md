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
    def login(self):
        return self.find_element_by_id("loginBtn")
```

### Initialization

The `View` class is initialized with either a `Callable[[], WebElement]` or a `WebDriver` instance though this requires manually setting the root element getter.

Both methods require a `Callable[[], WebElement]` to ensure that `root` never returns a `StaleElementReferenceError`.

```python
login = Login(lambda: driver.find_element_by_id("loginForm"))
```

or

```python
login = View(driver)
login.root = lambda: driver.find_element_by_id("loginForm")
```
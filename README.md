# vom

View Object Modal

## About

`vom` is a library for writing view objects for selenium tests/scripts

## Installation

```bash
$ pip install vom
```

## Usage

### Classes

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

### Prototyping Views

```python
from selenium import webdriver
from vom import View

driver = webdriver.Chrome()

login = View(lambda: driver.find_element_by_id("loginForm"))
login.username = login.find_element_by_name("username")
login.password = login.find_element_by_name("password")
login.login = login.find_element_by_id("loginBtn")
```

## Philosophy

### View Object vs Page Object

The term "page" is outdated in the context of modern web applications. The term "view" more aligned with the usage of self contained components (e.g. React, Angular, Vue). They represent the same concept however.

### Elements As Views

The `View` class mirrors the `WebElement` API only returning `View` instead of `WebElement` in methods like `find_element` & `find_elements`. This allow for powerful composability. The original `WebElement` is available from the `root` property.
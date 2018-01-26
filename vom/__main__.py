from selenium import webdriver
from vom import View

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=options)

    driver.get("http://example.com")

    page = View(lambda: driver.find_element_by_tag_name("div"))
    page.header = page.find_element_by_tag_name("h1")
    page.texts = page.find_elements_by_tag_name("p")

    page.click()

    print(page.header)

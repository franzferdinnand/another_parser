import dotenv
import os
import time
from selenium.common import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By

dotenv.load_dotenv("/Users/brian/PycharmProjects/another_parser/venv/.env")


def get_links(webpage_url):
    service = webdriver.FirefoxService()
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Firefox(service=service, options=options)

    driver.get(webpage_url)
    time.sleep(1)
    links_list = []

    try:
        cookies_window = driver.find_element(By.CLASS_NAME, "fc-button-label")
        cookies_window.click()
    except NoSuchElementException:
        pass

    link_elements = driver.find_elements(By.CLASS_NAME, "wizLnk")

    for element in link_elements:
        link = element.get_attribute("href")
        links_list.append(link)

    driver.close()

    return links_list


if __name__ == '__main__':
    print(get_links(os.getenv("URL").format("2")))

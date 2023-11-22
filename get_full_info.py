import subprocess

import dotenv
import os
import time

import pandas as pd
from selenium.common import NoSuchElementException, InvalidArgumentException
from selenium import webdriver
from selenium.webdriver.common.by import By

from clean_email import clean_mail
from fetch_email import fetch_email_from_pic
from fetch_links import get_links

dotenv.load_dotenv("./venv/.env")


def get_full_info(clients_url):
    firefox_service = webdriver.FirefoxService()
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    url = clients_url
    driver = webdriver.Firefox(service=firefox_service, options=options)

    full_info = []

    try:
        driver.get(url)
    except InvalidArgumentException:
        print(url)

    time.sleep(1)

    try:
        cookies_dialog = driver.find_element(By.CLASS_NAME, "fc-button-label")
        cookies_dialog.click()
    except NoSuchElementException:
        pass

    name = driver.find_element(By.XPATH, f'//h1[contains(@itemprop, "name")]').text
    street = driver.find_element(By.XPATH, f'//span[contains(@itemprop, "streetAddress")]').text
    post = driver.find_element(By.XPATH, f'//span[contains(@itemprop, "postalCode")]').text
    city = driver.find_element(By.XPATH, f'//span[contains(@itemprop, "addressLocality")]').text
    telephones = driver.find_elements(By.XPATH, f'//span[contains(@itemprop, "telephone")]')
    telephone = [tel.text for tel in telephones]
    branch = driver.find_element(By.CLASS_NAME, "br_link").text
    email = []

    try:
        emails = driver.find_elements(By.CLASS_NAME, "emlImg")
        for i in emails:
            with open(os.getenv("PATH_TO_IMAGE").format(i), 'wb') as file:
                file.write(i.screenshot_as_png)
            email_to_clean = fetch_email_from_pic(os.getenv("PATH_TO_IMAGE").format(i))
            cleaned_mail = clean_mail(email_to_clean)
            if not cleaned_mail == "not_email":
                email.append(cleaned_mail)
    except NoSuchElementException:
        email = "no_email"

    try:
        webpage = driver.find_element(By.XPATH, '//a[contains(@itemprop, "url")]').text
    except NoSuchElementException:
        webpage = "no_webpage"

    full_info.append(name)
    full_info.append(branch)
    full_info.append(street)
    full_info.append(post)
    full_info.append(city)
    full_info.append(webpage)
    full_info.append(telephone)
    full_info.append(email)

    driver.close()

    return full_info

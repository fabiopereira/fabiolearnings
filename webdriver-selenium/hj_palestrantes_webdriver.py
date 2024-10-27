from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

LINKEDIN_LINKS = '//a'
# LINKEDIN_LINKS = '//*[contains(@class, "fa-linkedin")]'

driver = webdriver.Chrome()
driver.get('https://hjconference.com.br/palestrantes/')
links = driver.element = driver.find_elements(By.XPATH, LINKEDIN_LINKS)
for link in links:
    print(f"Texto: {link.text}, URL: {link.get_attribute('href')}")
driver.quit()

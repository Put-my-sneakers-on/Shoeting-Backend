import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

search_url = "https://www.nike.com/kr/w/women-shoes-5e1x6zy7ok"

name_list = []
category_list = []
# serial_number_list = []
price_list = []
image_list = []
url_list = []

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser.get(search_url)

browser.implicitly_wait(2)

body = browser.find_element(By.CSS_SELECTOR, 'body')

for i in range(10):
    body.send_keys(Keys.PAGE_DOWN)
    body.send_keys(Keys.PAGE_DOWN)
    body.send_keys(Keys.PAGE_DOWN)
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

shoe = browser.find_elements(By.CLASS_NAME, "product-card__body")

for i in range(len(shoe)):
    name = shoe[i].find_element(By.CLASS_NAME, "product-card__title").text
    category = shoe[i].find_element(By.CLASS_NAME, "product-card__subtitle").text
    # serial_number = shoe[i].find_element(By.CLASS_NAME, "serial_number").text
    price = shoe[i].find_element(By.CLASS_NAME, "product-card__price").text
    image = shoe[i].find_element(By.CLASS_NAME, "product-card__hero-image").get_attribute('src')
    url = shoe[i].find_element(By.CLASS_NAME, "product-card__link-overlay").get_attribute('href')

    name_list.append(name)
    category_list.append(category)
    # serial_number_list.append(serial_number)
    price_list.append(price)
    image_list.append(image)
    url_list.append(url)

browser.close()

data = {"name": name_list, "category": category_list, "price": price_list, "image": image_list, "url": url_list}
df = pd.DataFrame(data)
print(df.head(5))

df.to_csv("nike.csv", encoding="utf-8-sig")

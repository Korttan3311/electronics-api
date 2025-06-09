from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def scrape_courts():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.courts.com.sg/televisions")
    time.sleep(5)

    products = []
    elements = driver.find_elements(By.CLASS_NAME, "product-tile")
    for el in elements:
        try:
            name = el.find_element(By.CLASS_NAME, "product-title").text
            price = el.find_element(By.CLASS_NAME, "product-price").text
            link = el.find_element(By.TAG_NAME, "a").get_attribute("href")
            products.append({
                "name": name,
                "price": price,
                "link": link,
                "store": "Courts"
            })
        except:
            continue

    driver.quit()
    return products

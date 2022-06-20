from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)


driver.get("https://www.wowt.com/weather")

hours = driver.find_elements(by=By.CSS_SELECTOR, value="div.hour")
for hour in hours:
    print(hour.text)

driver.close()

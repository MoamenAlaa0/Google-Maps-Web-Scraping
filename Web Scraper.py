from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import pandas as pd

url = "https://www.google.com/maps/search/malls/@31.152474,29.9910573,11z?hl=en"

option =  webdriver.ChromeOptions() 

option.add_argument("--headless")
option.add_argument('--disable-gpu')
option.add_argument("start-maximized")
option.add_argument("disable-infobars")
option.add_argument("--disable-extensions")
option.add_argument("window-size=1920x1080")
option.add_argument("--no-sandbox")
option.add_argument("--disable-setuid-sandbox")

driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=option)
driver.get(url)

for i in range(3,500,3):
    try:
        last_review = driver.find_elements(By.CSS_SELECTOR, 'div[jstcache="192"]')
        driver.execute_script('arguments[0].scrollIntoView(true);', last_review[i])
        time.sleep(5)
    except: break

anchores = driver.find_elements(By.CSS_SELECTOR, 'div[jstcache="192"] > div > a')
print(len(anchores))

links = [link.get_attribute('href') for link in anchores]
driver.quit()

malls = [] 

for link in links:
    time.sleep(3)
    
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=option)
    driver.get(link)
    print('Strat ...')
    
    driver.implicitly_wait(50)
    
    try:
        title = driver.find_element(By.TAG_NAME, 'h1').text
        print(title)
        address = driver.find_element(By.CSS_SELECTOR, 'button[data-item-id="address"]').get_attribute('aria-label').strip('Address: ')
    except: 
        driver.quit()
        continue
    
    driver.quit()
    data = {'title':title, 'address': address, 'link': link}
    malls.append(data)
    
Data = pd.DataFrame(malls)
Data.to_csv('alexandria_malls.csv', index=False)
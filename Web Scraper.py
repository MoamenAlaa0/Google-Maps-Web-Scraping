from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import pandas as pd

# main link: malls in Alexandria city
url = "https://www.google.com/maps/search/malls/@31.152474,29.9910573,11z?hl=en"

# Creating Chrome Driver session object
option =  webdriver.ChromeOptions() 

# The Headless mode is a feature which allows the execution of a full version of the Chrome Browser
# It provides the ability to control Chrome via external programs
# The headless mode can run on servers without the need for dedicated display or graphics
option.add_argument("--headless")
# Needed if running Chrome in headless mode on Windows.
# https://developer.chrome.com/blog/headless-chrome/
option.add_argument('--disable-gpu')
# Maximize the chrome
option.add_argument("start-maximized")
option.add_argument("window-size=1920x1080")
option.add_argument("disable-infobars")
option.add_argument("--disable-extensions")
option.add_argument("--no-sandbox")
option.add_argument("--disable-setuid-sandbox")

# Open the external Chrome Driver
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=option)
# Get request to the webpage
driver.get(url)

# Scroll down until the element with div[jstcache="192"] selector appears 
# If the code throw an exception like NoSuchElementException, the loop will break because there is no another elements will appear.
for i in range(3,500,3):
    try:
        last = driver.find_elements(By.CSS_SELECTOR, 'div[jstcache="192"]')
        driver.execute_script('arguments[0].scrollIntoView(true);', last[i])
        time.sleep(5)
    except: break

# Get the links of all malls
anchores = driver.find_elements(By.CSS_SELECTOR, 'div[jstcache="192"] > div > a')
print(len(anchores))

links = [link.get_attribute('href') for link in anchores]
# Quit from all the browser windows and terminates the WebDriver session
driver.quit()

malls = [] 

for link in links:
    # Delay three second
    time.sleep(3)
    
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=option)
    driver.get(link)
    print('Strat ...')
    
    # waiting up to 50 seconds before it gives up searching for an element on a page
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

# Saving data as csv file
Data = pd.DataFrame(malls)
Data.to_csv('alexandria_malls.csv', index=False)
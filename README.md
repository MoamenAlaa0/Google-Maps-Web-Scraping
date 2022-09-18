## :globe_with_meridians: Google Maps Web Scraping
Scraping all malls in alexandria using [selenium](https://selenium-python.readthedocs.io/)  

The aim of this code: scroll down until the element with div[jstcache="192"] selector appears
``` python
for i in range(3,500,3):
    try:
        last = driver.find_elements(By.CSS_SELECTOR, 'div[jstcache="192"]')
        driver.execute_script('arguments[0].scrollIntoView(true);', last[i])
        time.sleep(5)
    except: break
```

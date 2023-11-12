from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Keep browser open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, value='cookie')

# Get upgrade item ids.
items = driver.find_elements(by=By.CSS_SELECTOR, value="#store div")
item_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 5
five_min = time.time() + 60*5  # 5 minutes

while(1):
    cookie.click()

    if time.time() > timeout:
        money = driver.find_element(By.ID, value='money').text
        prices = driver.find_elements(By.CSS_SELECTOR, value="#store b")

        item_prices = []

        for price in prices:
            txt = price.text
            if txt != "":
                cost = int(txt.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        # Create dictionary of store items and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        if "," in money:
            money = money.replace(",", "")
            print(f'money:{money}')
        
        cookie_price = int(money)

        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_price >= cost:
                affordable_upgrades[cost] = id

        # Purchase the most expensive affordable upgrade
        if affordable_upgrades:
            highest_price_affordable_upgrade = max(affordable_upgrades)
            to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

            driver.find_element(by=By.ID, value=to_purchase_id).click()

        # Add another 5 seconds until the next check
        timeout = time.time() + 5

        # After 5 minutes stop the bot and check the cookies per second count.
    if time.time() > five_min:
        cookie_per_s = driver.find_element(by=By.ID, value="cps").text
        print(cookie_per_s)
        five_min = time.time() + 60*5
        #break
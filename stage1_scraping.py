from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv

URL = "https://www.spinny.com/used-suv-cars-in-hyderabad/s/"

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get(URL)

time.sleep(5)

print("✅ Page Opened")

# 🔽 SCROLL TO LOAD ALL CARS
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

print("✅ Fully Loaded")

# 🔽 GET ALL CAR LINKS (IMPORTANT FIX)
cars = driver.find_elements(By.XPATH, "//a[contains(@href,'/buy-used-cars')]")

print("Total Cars Found:", len(cars))

links = []
for car in cars:
    link = car.get_attribute("href")
    if link and link not in links:
        links.append(link)

print("Unique Cars:", len(links))

# 🔽 CSV SETUP
with open("spinny_suv_full.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Name",
        "Price",
        "Overview",
        "Quality Report"
    ])

    count = 0

    for link in links:
        try:
            driver.get(link)
            time.sleep(4)

            name = ""
            price = ""
            overview = ""
            quality = ""

            # 🔽 NAME
            try:
                name = driver.find_element(By.TAG_NAME, "h1").text
            except:
                pass

            # 🔽 PRICE
            try:
                price = driver.find_element(By.XPATH, "//div[contains(text(),'₹')]").text
            except:
                pass

            # 🔽 OVERVIEW
            try:
                overview_elem = driver.find_element(
                    By.XPATH,
                    "//section[contains(.,'Overview')]"
                )
                overview = overview_elem.text
            except:
                pass

            # 🔽 QUALITY REPORT
            try:
                quality_elem = driver.find_element(
                    By.XPATH,
                    "//section[contains(.,'Quality')]"
                )
                quality = quality_elem.text
            except:
                pass

            writer.writerow([name, price, overview, quality])

            count += 1
            print(f"✅ {count} Done: {name}")

        except Exception as e:
            print("❌ Error:", e)

print("🎉 DONE:", count)

driver.quit()
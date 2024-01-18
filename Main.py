import time
import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs4

home_address="Ūnijas iela 93"
faculty_address="Zunda krastmala 8"

service = Service()
option = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=option)


while True:
    action = input(f"Izvēlieties uz kurieni dosities:\n1\tUz universitāti\n2\tUz mājām\n")
    if action == "1":
        start = home_address
        end = faculty_address
        break
    elif action == "2":
        start = faculty_address
        end = home_address
        break
    else:
        print("Kļūda ievadē")

url = "https://saraksti.rigassatiksme.lv/index.html#plan//"
driver.get(url)
delay = 5
wait = WebDriverWait(driver, delay)
    
# Sākumpunkta ievade
find = wait.until(ec.presence_of_element_located((By.ID, "inputStart")))
find.click()
find.send_keys(start)

wait.until(ec.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{start[:4]}')]")))
find = driver.find_element(By.ID, "geocaching-results")
find = find.find_element(By.XPATH, ".//a")
find.click()

# Galapunkta ievade
find = driver.find_element(By.ID, "inputFinish")
find.click()
find.send_keys(end)
    
wait.until(ec.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{end[:4]}')]")))
find = driver.find_element(By.ID, "geocaching-results")
find = find.find_element(By.XPATH, ".//a")
find.click()

# Resultātu iegūšana
find = driver.find_element(By.ID, "buttonSearch")
find.click()

# Maršruta opciju nosaukumu un kopējā laika iegūšana
wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "routes_scroller")))
time.sleep(1)
find = driver.find_element(By.ID, "divContentPlannerResults")
options = find.find_elements(By.TAG_NAME, "table")
options_list = [option.text for option in options]

# Maršruta detaļu (sīkākas informācijas) iegūšana un tīrīšana
route_details = find.find_elements(By.CLASS_NAME, "RouteDetails")
route_list = []
for route in route_details:
    inner_html = route.get_attribute('innerHTML')
    text = bs4(inner_html, 'html.parser').get_text(separator=' ', strip=True)
    cleaned_text = text.replace('\xa0', ' ')
    route_list.append(cleaned_text)

# Teksta sadale formatēšanai
route_detail_list = [re.split(r'(?<=min\.\))', route) for route in route_list]

# Teksta izvade
for i in range(len(options_list)):
    print(f"---------------------------\n{options_list[i]}")
    for j in range(len(route_detail_list[i])-1):
        print(f"{j+1}.\t{route_detail_list[i][j].lstrip()}")
    print()

if options_list == []:
    print("Netika atrasts neviens maršruts")






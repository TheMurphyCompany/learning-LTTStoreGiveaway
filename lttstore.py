from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
#curl
import requests
from lxml import html
#audio alarm
from playsound import playsound
from threading import Thread

def play_music():
    playsound('BUYME.mp3')

def play_alarm():
    playsound('notification.mp3')

#waits
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import random
import time

# open chrome


options = Options()
options.add_argument("user-data-dir=C:\\Users\\admin\\appdata\\local\\google\\chrome\\User Data")
driver = webdriver.Chrome(chrome_options=options)

###LOGIN###
driver.get(
    "https://www.lttstore.com/collections/all/?sort_by=created-descending")


#loop do loop of this in background until we find the magic number 1!, then refresh the page
found = False
url = ""
attempt = 0
last_price = 0.00
while not found:
    pageContent = requests.get('https://www.lttstore.com/collections/all/?sort_by=created-descending')    
    tree = html.fromstring(pageContent.content)
    price = tree.xpath("(//span[@class='money'])")
    items = [0,1,2,3,4,5,6,7,8,9,10]
    newest_price = float(price[0].text.replace(' USD','')[1:])
    if newest_price != last_price :
        alarm_thread = Thread(target=play_alarm)
        alarm_thread.start()
        last_price = newest_price
        print('Found new price at : ' + str(newest_price))

    for x in items:
        try:
            free3080ti = float(price[x].text.replace(' USD','')[1:]) < 3
            if free3080ti :
                url = tree.xpath("//h2[@class='ProductItem__Title Heading']/a")[x].attrib['href']
                found=True
                break
        except:
            print('OH OH, WE BEEN COCKED BLOCKED!')
            music_thread = Thread(target=play_music)
            music_thread.start()
            time.sleep(120)

    attempt+=1
    print(str(attempt))
      
    if attempt%100==0 : 
        print("last price value :" + str(float(price[0].text.replace(' USD','')[1:])))
    time.sleep(random.uniform(1.0, 2.0))

if found:
    music_thread = Thread(target=play_music)
    music_thread.start()
    driver.get(
    "https://www.lttstore.com/"+url)
   
    element = WebDriverWait(driver, 5).until( EC.presence_of_element_located((By.CLASS_NAME, "shopify-payment-button")))
    clickElement = driver.find_element_by_class_name("shopify-payment-button")
    clickElement.click()
    element = WebDriverWait(driver, 5).until( EC.presence_of_element_located((By.ID, "continue_button")))
    clickElement = driver.find_element_by_id("continue_button")
    clickElement.click()
    time.sleep(0.5)
    element = WebDriverWait(driver, 5).until( EC.presence_of_element_located((By.ID, "continue_button")))
    clickElement = driver.find_element_by_id("continue_button")
    clickElement.click()

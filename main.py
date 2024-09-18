from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
import argparse
import time
from datetime import datetime

parser = argparse.ArgumentParser()

parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('sport')
parser.add_argument('date')
parser.add_argument('hour')

args = parser.parse_args()


driver = webdriver.Firefox()
wait = WebDriverWait(driver, 2)  # initialization
action = ActionChains(driver)

driver.get("https://sites.uclouvain.be/uclsport/seances")  # open the site
driver.maximize_window()

time.sleep(.5)
driver.find_element(By.XPATH, "/html/body/div[1]/div/div/nav/div[1]/div/div/nav/div[2]/ul/li[3]/a/a").click()
time.sleep(1.5)

driver.find_element(By.XPATH, '//*[@id="input-account"]').send_keys(args.username)  # mail autocompletion
driver.find_element(By.XPATH, '//*[@id="input-password"]').send_keys(args.password)  # password autocompletion
driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div/div/form/div[2]/button").click()  # click on sign in
time.sleep(5)

element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/nav/div[2]/div/div[1]/div/h6')
web_date = element.text.split(" ")[2][:5]

while web_date!=args.date:
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div/nav/div[2]/div/div[1]/div/h6/a[2]/span").click() # change the date
    element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/nav/div[2]/div/div[1]/div/h6') # find the date
    web_date = element.text.split(" ")[2][:5] # update the date

driver.find_element(By.XPATH, "/html/body/div[1]/div/div/nav/div[2]/div/div[2]/div/a/span").click() # click on the search button
driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div/div/select/option[2]").click()  # select louvain la neuve : change option number to the one you want
driver.find_element(By.XPATH, '//input[@placeholder="filtre"]').send_keys(args.sport) # enter the sport
driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div/footer/button").click() # close the searching tab

list_sport = []

try:
    i=1
    while True:
        info = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[{0}]/div[1]/div[1]/div/div[1]/div/p'.format(str(i)))
        list_sport.append(str(info.text.split(" ")[0]) + ">" + str(info.text.split(" ")[2]) + str(i))
        i += 1
except:
    pass

for option in list_sport:
    if args.hour in option:
        index_sport = option[-1]

driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div[{0}]/div[1]/div[2]/span".format(index_sport)).click() # open chosen sport tab

while True:
    try:
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div[{0}]/div[2]/div/div/div/div/div[2]/div/div/button".format(index_sport)).click() # click register
        break
    except:
        driver.refresh()
        time.sleep(5)

driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div/footer/div/button[2]".format(index_sport)).click() # click ok to register
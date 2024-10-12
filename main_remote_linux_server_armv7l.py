from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

import argparse
import time
from datetime import timedelta
from datetime import datetime

parser = argparse.ArgumentParser()

parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('sport')
parser.add_argument('date')
parser.add_argument('hour')

args = parser.parse_args()

if len(args.date)!=5 or args.date[2]!="/" or not args.date[:2].isdigit() or not args.date[-2:].isdigit():
    raise ValueError("The date format string should be like ../.., if the day/month number is single digit, add a zero, i.e. 7/1 -> 07/01")

hour = args.hour
if len(hour)!=11 or not hour[:2].isdigit() or not hour[3:5].isdigit() or not hour[6:8].isdigit() or not hour[9:].isdigit() or hour[2]!=":" or hour[5]!="-" or hour[8]!=":":
    raise ValueError("The hour format string should be like ..:..-..:.., e.g. 21:30-23:00")

opts = Options()
opts.add_argument("--headless")
service = Service("/usr/bin/geckodriver")
service=Service()

driver = webdriver.Firefox(options=opts, service=service)
wait = WebDriverWait(driver, 2)  # initialization
action = ActionChains(driver)

print("Driver initialized")

driver.get("https://sites.uclouvain.be/uclsport/seances")  # open the site
driver.maximize_window()

print("Website acquired")

time.sleep(.5)
driver.find_element(By.XPATH, "/html/body/div[1]/div/div/nav/div[1]/div/div/nav/div[2]/ul/li[3]/a/a").click()
time.sleep(1.5)

driver.find_element(By.XPATH, '//*[@id="input-account"]').send_keys(args.username)  # mail autocompletion
driver.find_element(By.XPATH, '//*[@id="input-password"]').send_keys(args.password)  # password autocompletion
driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div/div/form/div[2]/button").click()  # click on sign in
time.sleep(5)

print("logged in")

element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/nav/div[2]/div/div[1]/div/h6')
web_date = element.text.split(" ")[2][:5]
current_date = web_date
print("date", web_date)

while web_date!=args.date:
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div/nav/div[2]/div/div[1]/div/h6/a[2]/span").click() # change the date
    element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/nav/div[2]/div/div[1]/div/h6') # find the date
    web_date = element.text.split(" ")[2][:5] # update the date

print("date successfully changed", web_date)

driver.find_element(By.XPATH, "/html/body/div[1]/div/div/nav/div[2]/div/div[2]/div/a/span").click() # click on the search button
driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div/div/select/option[2]").click()  # select louvain la neuve : change option number to the one you want
driver.find_element(By.XPATH, '//input[@placeholder="filtre"]').send_keys(args.sport) # enter the sport
driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div/footer/button").click() # close the searching tab

list_sport = []

try:
    i=1
    while True:
        info = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[{0}]/div[1]/div[1]/div/div[1]/div/p'.format(str(i)))
        list_sport.append(str(info.text.split(" ")[0]) + "-" + str(info.text.split(" ")[2]) + str(i))
        i += 1
except:
    pass

for option in list_sport:
    if args.hour in option:
        index_sport = option[-1]

driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div[{0}]/div[1]/div[2]/span".format(index_sport)).click() # open chosen sport tab

print("tab opened")

days_difference = datetime(2024, int(args.date[-2:]), int(args.date[:2])) - datetime(2024, int(current_date[-2:]), int(current_date[:2]))
print(days_difference)

seconds_to_wait = (datetime(2024, int(current_date[-2:]), int(current_date[:2])) + timedelta(days=days_difference.days-7) - datetime.now()).total_seconds()
print("time to wait until the registration opens", seconds_to_wait)

if seconds_to_wait-60 > 0:
    print("Waiting midnight...")
    time.sleep(seconds_to_wait-60) # wait until there is one minute left to register

print("Now waiting actively")

while True:
    try:
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div[{0}]/div[2]/div/div/div/div/div[2]/div/div/button".format(index_sport)).click() # click register
        driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div/footer/div/button[2]".format(index_sport)).click() # click ok to register
        break
    except:
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div[{0}]/div[1]/div[2]/span".format(index_sport)).click()
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div[{0}]/div[1]/div[2]/span".format(index_sport)).click()
        time.sleep(1)

print("registration finished successfully")

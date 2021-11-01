import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import re
import csv

PATH = "C:\Program Files (x86)\chromedriver.exe"
START_YEAR = "2015"
START_MONTH = "01"
END_YEAR = "2019"
END_MONTH = "01"
driver = webdriver.Chrome(PATH)
data = []

while True:
    driver.get(f"https://www.espn.com/soccer/fixtures/_/date/{START_YEAR}{START_MONTH}01")
    time.sleep(1)
    i = 1
    btn = driver.find_element_by_xpath("/html/body/div[10]/div[3]/div/div/div[3]/button")
    btn.click()
    while True:
        league = 2
        while True:
            try:
                time.sleep(1)
                print("tried")
                ht = driver.find_element_by_xpath(
                    f"/html/body/div[5]/section/section/div/section/div/div/div[2]/div[{league}]/table/tbody/tr/td[1]/a/span").text
                at = driver.find_element_by_xpath(
                    f"/html/body/div[5]/section/section/div/section/div/div/div[2]/div[{league}]/table/tbody/tr/td[2]/a/span").text
                print(ht + "-" + at)
            except:
                round = 1
                print(round)
                while True:
                    time.sleep(1)
                    ht = driver.find_element_by_xpath(f"/html/body/div[5]/section/section/div/section/div/div/div[2]/div[{league}]/table/tbody/tr[{round}]/td[1]/a/span").text
                    at = driver.find_element_by_xpath(f"/html/body/div[5]/section/section/div/section/div/div/div[2]/div[{league}]/table/tbody/tr[{round}]/td[2]/a/span").text
                    print(ht + "-" + at)
                    round += 1
            league += 1
        break
    break
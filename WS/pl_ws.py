import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import re
import csv

PATH = "C:\Program Files (x86)\chromedriver.exe"
START_YEAR = 2015
START_MONTH = 1
END_YEAR = 2019
END_MONTH = 1
driver = webdriver.Chrome(PATH)


while True:
    driver.get("https://www.premierleague.com/results")
    time.sleep(1)
    cookie = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[1]/div[5]/button[1]")
    cookie.click()
    time.sleep(1)
    ex = driver.find_element(By.XPATH, "/html/body/main/div[1]/nav/a[2]")
    ex.click()
    time.sleep(1)
    season = driver.find_element(By.XPATH, "/html/body/main/div[3]/div[1]/section/div[3]")
    season.click()
    time.sleep(1)
    choice = driver.find_element(By.XPATH, "/html/body/main/div[3]/div[1]/section/div[3]/ul/li[7]")
    choice.click()

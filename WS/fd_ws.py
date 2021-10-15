import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import Select
import time
import re
import csv

options = ChromeOptions()
options.add_argument("--disable-notifications")
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH, options=options)
user = "jorgen.farner@gmail.com"
pwd = "wUvDcH3W63Q4VMQ"

# Football database
# https://www.footballdatabase.eu/en/match/summary/2160992-nagoya_grampus-tokushima_vortis
# pw: wUvDcH3W63Q4VMQ
# FM Data
# https://sortitoutsi.net/


HEADERS = ["date", "home_team", "away_team", "home_score", "away_score", "home_lineup", "away_lineup"]
MONTHS = {"January" : 1, "February" : 2, "March" : 3, "April": 4, "May" : 5, "June": 6, "July" : 7, "August" : 8, "September" : 9, "October" : 10, "November" : 11, "December" : 12}
START_MONTH = 1
START_YEAR = 2015
data = []


driver.get("https://www.footballdatabase.eu/en/fixtures")
time.sleep(1)
# login = driver.find_element_by_xpath("/html/body/header/div[3]/div[2]/div[1]/a")
# login.click()
alr = driver.find_element_by_xpath("/html/body/div[7]/div[3]/form/div[7]/a")
alr.click()
login_user = driver.find_element_by_id("login_email")
login_user.send_keys(user)
login_pwd = driver.find_element_by_id("login_password")
login_pwd.send_keys(pwd)
login = driver.find_element_by_id("login_connect")
login.click()
time.sleep(1)
round = 1
while True:
    btn = driver.find_element_by_xpath("/html/body/div[6]/div[2]/div[1]/div/div[2]/div[2]/h3/a")
    btn.click()
    time.sleep(1)
    slc = Select(driver.find_element_by_class_name("roundlist"))
    try:
        slc.select_by_visible_text(f"Round {round}")
    except:
        print(f"Unable to select {round} from dropdown")
        break
    print(f"successfully selected {round} from dropdown")
    rows = len(driver.find_elements_by_class_name("score"))
    row = 0
    while True:
        game = driver.find_elements_by_class_name("score")[row]
        info = []
        game.click()
        time.sleep(1)
        date_str = driver.find_element_by_class_name("date").text
        day = str(int(re.findall("(\d\d),", date_str)[0]))
        month_str = re.findall("([A-Za-z]+) ", date_str)[0]
        month = MONTHS[month_str]
        year = re.findall(", (\d\d\d\d)", date_str)[0]
        date = f"{day}.{month}.{year}"
        h = driver.find_element_by_xpath("/html/body/div[6]/div/div[2]/main/div[2]/div[2]/div[1]/div[1]/a/h2").text
        a = driver.find_element_by_xpath("/html/body/div[6]/div/div[2]/main/div[2]/div[2]/div[1]/div[3]/a/h2").text
        score = driver.find_element_by_xpath("/html/body/div[6]/div/div[2]/main/div[2]/div[2]/div[1]/div[2]/h2").text
        h_s = re.findall("(\d+) -", score)[0]
        a_s = re.findall("- (\d+)", score)[0]
        h_t = []
        a_t = []
        for team in [1,2]:
            for player in range(2,13):
                player = driver.find_element_by_xpath(f"/html/body/div[6]/div/div[2]/main/div[5]/div[1]/div[{team}]/div[2]/div/table/tbody/tr[{player}]/td[4]/a").text
                if team == 1:
                    h_t.append(player)
                else:
                    a_t.append(player)
        info.append(date)
        info.append(h)
        info.append(a)
        info.append(h_s)
        info.append(a_s)
        info.append(h_t)
        info.append(a_t)
        print(info)
        data.append(info)
        driver.back()
        time.sleep(1)
        driver.refresh()
        time.sleep(1)
        row += 1
        if row >= rows:
            break
    round += 1

print(data)
driver.quit()

file = open("../data/misc/fd_gd_dup.csv", "w", encoding="utf-8", newline="")
writer = csv.writer(file)
writer.writerow(HEADERS)
for row in data:
    writer.writerow(row)
file.close()

import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import csv
PATH = "C:\Program Files (x86)\chromedriver.exe"
START_YEAR = 2015
START_MONTH = 1
END_YEAR = 2019
END_MONTH = 1
driver = webdriver.Chrome(PATH)
# Football database
# https://www.footballdatabase.eu/en/match/summary/2160992-nagoya_grampus-tokushima_vortis
# pw: wUvDcH3W63Q4VMQ
# FM Data
# https://sortitoutsi.net/
#while

VALID_COMPS = ["UEFA Champions League", "UEFA Europa League", "UEFA Super Cup", "European Qualifiers", "UEFA Regions' Cup", "UEFA Europa Conference League", "Friendly Matches", "FIFA World Cup", "UEFA Nations League", "UEFA EURO"]
HEADERS = ["date", "home_team", "away_team", "home_score", "away_score", "home_lineup", "away_lineup"]
data = []
date = datetime.datetime(START_YEAR, START_MONTH, 1)
comps = []
while True:
    driver.get(f"https://www.uefa.com/livescores/?date={date.year}-{date.month}-{date.day}")
    time.sleep(1)
    #year = re.findall("\d\d\d\d", driver.find_element_by_xpath(
     #   "/html/body/div[3]/div/div/div[2]/section/div/div/div/div/div/div/div[1]/div/div[2]/a/div").text)
    #if year == str(END_YEAR):
    #    break
    x_path = "/html/body/div[3]/div/div/div[2]/section/div/div/div/div/div/div/div[3]"
    matches = driver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/section/div/div/div/div/div/div/div[3]")
    if matches.text == "No matches are scheduled for today.":
        date += datetime.timedelta(days=1)
        continue
    else:
        i = 1
        while True:
            try:
                x_path = f"/html/body/div[3]/div/div/div[2]/section/div/div/div/div/div/div/div[3]/div[{i}]/div/div/div/div/a/span"
                comp_info = driver.find_element_by_xpath(x_path).text
                if comp_info not in comps:
                    comps.append(comp_info)
                if comp_info in VALID_COMPS:
                    info = []
                    score = driver.find_element_by_xpath(f"/html/body/div[3]/div/div/div[2]/section/div/div/div/div/div/div/div[3]/div[{i}]/div/a/div/div[4]/span[2]").text
                    h = driver.find_element_by_xpath(f"/html/body/div[3]/div/div/div[2]/section/div/div/div/div/div/div/div[3]/div[{i}]/div/a/div/div[3]/div/div/span").text
                    a = driver.find_element_by_xpath(f"/html/body/div[3]/div/div/div[2]/section/div/div/div/div/div/div/div[3]/div[{i}]/div/a/div/div[5]/div/div/span").text
                    h_s = re.findall("(\d+)-", score)[0]
                    a_s = re.findall("-(\d+)", score)[0]
                    game = driver.find_element_by_xpath(f"/html/body/div[3]/div/div/div[2]/section/div/div/div/div/div/div/div[3]/div[{i}]")
                    game.click()
                    time.sleep(1)
                    h_t = []
                    a_t = []
                    for team in [1,2]:
                        for player in range(1,12):
                            p = driver.find_element_by_xpath(f"/html/body/div[3]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div/ul[{team}]/li[{player}]/a").get_attribute("title")
                            if team == 1:
                                h_t.append(p)
                            else:
                                a_t.append(p)
                    info.append(f"{date.day}.{date.month}.{date.year}")
                    info.append(h)
                    info.append(a)
                    info.append(h_s)
                    info.append(a_s)
                    info.append(h_t)
                    info.append(a_t)
                    data.append(info)
                    driver.back()
                    print(info)
                    time.sleep(1)
                i +=1
            except:
                break
    date += datetime.timedelta(days=1)
    if date.year == END_YEAR and date.month == END_MONTH:
        break

driver.quit()
comp_s = ",".join(comps)
with open("../data/misc/comps.txt", "w", encoding="utf-8") as f:
    f.write(comp_s)

file = open("../data/misc/uefa_gd_2015-2018.csv", "w", encoding="utf-8", newline="")
writer = csv.writer(file)
writer.writerow(HEADERS)
for row in data:
    writer.writerow(row)
file.close()
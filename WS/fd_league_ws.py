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
SEASONS = ["2015/2016"]
#,"2016/2017","2017/2018","2018/2019"]

ligue_1 = "https://www.footballdatabase.eu/en/competition/overall/10570-ligue_1_conforama/2017-2018/160826-journee_1"
la_liga = "https://www.footballdatabase.eu/en/competition/overall/14983-la_liga_santander/2021-2022/-"
serie_a = "https://www.footballdatabase.eu/en/competition/overall/14904-serie_a_tim/2021-2022/-"
bundesliga = "https://www.footballdatabase.eu/en/competition/overall/14901-bundesliga/2021-2022/-"
premier_league = "https://www.footballdatabase.eu/en/competition/overall/14896-premier_league/2021-2022/247565-journee_1"
leagues = [la_liga, serie_a, bundesliga, premier_league]
#, la_liga, serie_a, bundesliga, premier_league
logged_in = False
file = open("data/fd_gd.csv", "a", encoding="utf-8", newline="")
writer = csv.writer(file)
#writer.writerow(HEADERS)
for league in leagues:
    driver.get(league)
    time.sleep(1)
    # login = driver.find_element_by_xpath("/html/body/header/div[3]/div[2]/div[1]/a")
    # login.click()
    if not logged_in:
        alr = driver.find_element_by_class_name("connect")
        alr.click()
        login_user = driver.find_element_by_id("login_email")
        login_user.send_keys(user)
        login_pwd = driver.find_element_by_id("login_password")
        login_pwd.send_keys(pwd)
        login = driver.find_element_by_id("login_connect")
        login.click()
        logged_in = True
    time.sleep(1)
    for season in SEASONS:
        dropdown = driver.find_element_by_class_name("seasons")
        dropdown.click()
        time.sleep(1)
        #sl = WebDriverWait(driver,10).until((ec.visibility_of_element_located((By.XPATH(f"// li[contains(text(),'{season}')]")))))
        sl = driver.find_element_by_xpath(f"// li[contains(text(),'{season}')]")
        sl.click()
        time.sleep(1)
        round = 20
        while True:
            btn = driver.find_element_by_class_name("plus")
            btn.click()
            time.sleep(1)
            slc_r = Select(driver.find_element_by_class_name("roundlist"))
            try:
                slc_r.select_by_visible_text(f"Round {round}")
            except:
                print(f"Unable to select {round} from dropdown")
                break
            rows = len(driver.find_elements_by_class_name("score"))
            row = 0
            data = []
            while True:
                try:
                    game = driver.find_elements_by_class_name("score")[row]
                except:
                    break
                info = []
                game.click()
                time.sleep(1)
                date_str = driver.find_element_by_class_name("date").text
                day = str(int(re.findall("(\d\d),", date_str)[0]))
                month_str = re.findall("([A-Za-z]+) ", date_str)[0]
                month = MONTHS[month_str]
                year = re.findall(", (\d\d\d\d)", date_str)[0]
                date = f"{day}.{month}.{year}"
                teams = driver.find_elements_by_class_name("team")
                h = teams[0].text
                a = teams[1].text
                try:
                    score = driver.find_element_by_xpath("/html/body/div[6]/div/div[2]/main/div[2]/div[2]/div[1]/div[2]/h2").text
                except:
                    score = driver.find_element_by_xpath(
                        "/html/body/div[7]/div/div[2]/main/div[2]/div[2]/div[1]/div[2]/h2").text
                h_s = re.findall("(\d+) -", score)[0]
                a_s = re.findall("- (\d+)", score)[0]
                h_t = []
                a_t = []
                for team in [1,2]:
                    for player in range(2,13):
                        try:
                            player = driver.find_element_by_xpath(f"/html/body/div[6]/div/div[2]/main/div[5]/div[1]/div[{team}]/div[2]/div/table/tbody/tr[{player}]/td[4]/a").text
                        except:
                            player = driver.find_element_by_xpath(f"/html/body/div[7]/div/div[2]/main/div[5]/div[1]/div[{team}]/div[2]/div/table/tbody/tr[{player}]/td[4]/a").text
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
            time.sleep(1)
            for row in data:
                writer.writerow(row)
file.close()
driver.quit()



import csv


with open("gd2017.csv", "r", encoding="utf-8") as f:
    for row in f.readlines():
        print(row)
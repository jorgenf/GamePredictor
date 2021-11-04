import csv
import unicodedata
import pandas as pd
import unicodedata
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
sns.set()

'''
s = "Bøjan-Letić"
t = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("utf-8")
print(t)
if t == "Bojan Letic":
    print("COOL")



df = pd.read_csv("C:/Users/jorge/PycharmProjects/WebScraper/data/game_data.csv", index_col=False)


df["home_lineup"] = df["home_lineup"].apply(lambda x : unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode("utf-8"))
df["away_lineup"] = df["away_lineup"].apply(lambda x : unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode("utf-8"))

'''

matches_kept = [99.5, 98.3, 97, 96, 94.3, 92.5, 90.5,86.0,75.3, 53.4, 16.9]
threshold = [1,2,3,4,5,6,7,8,9,10,11]

plt.plot(threshold, matches_kept)
plt.xticks(range(12), fontsize=25)
plt.yticks(np.arange(0,110,10), fontsize=25)
plt.xlabel("Player threshold", fontsize=30)
plt.ylabel("Matches kept (%)", fontsize=30)
plt.title("Retained matches", fontsize=35)
plt.show()
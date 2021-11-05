import csv
import unicodedata
import pandas as pd
import unicodedata
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
import itertools
sns.set()
cm = 1/2.54
plt.rc('axes', titlesize=10)
plt.rc('axes', labelsize=10)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('figure', titlesize=14)
plt.rcParams['figure.figsize'] = (15*cm, 8*cm)

'''
data = [[0.3534675615212528, 0.378076062639821, 0.41387024608501116],
[0.36017897091722595, 0.36017897091722595, 0.34675615212527966],
[0.41834451901565994, 0.3691275167785235, 0.3870246085011186],
[0.3982102908277405, 0.36017897091722595, 0.3982102908277405],
[0.37360178970917224, 0.39373601789709173, 0.39373601789709173],
[0.3982102908277405, 0.4161073825503356, 0.4004474272930649],
[0.40268456375838924, 0.39149888143176736, 0.39373601789709173],
[0.3534675615212528, 0.37360178970917224, 0.39149888143176736],
[0.3982102908277405, 0.3982102908277405, 0.3825503355704698],
[0.4004474272930649, 0.40268456375838924, 0.407158836689038],
[0.3825503355704698, 0.3982102908277405, 0.378076062639821],
[0.378076062639821, 0.40939597315436244, 0.3982102908277405],
[0.3870246085011186, 0.37360178970917224, 0.39373601789709173],
[0.39373601789709173, 0.378076062639821, 0.39373601789709173],
[0.3825503355704698, 0.4116331096196868, 0.40268456375838924],
[0.407158836689038, 0.40492170022371365, 0.36465324384787473],
[0.3713646532438479, 0.42058165548098436, 0.40492170022371365],
[0.4250559284116331, 0.3870246085011186, 0.44742729306487694],
[0.37583892617449666, 0.3668903803131991, 0.37360178970917224],
[0.40939597315436244, 0.3624161073825503, 0.378076062639821]]

d1 = 0
d2 = 0
d3 = 0

for d in data:
    d1 += d[0]
    d2 += d[1]
    d3 += d[2]

print(d1/len(data))
print(d2/len(data))
print(d3/len(data))



df = pd.read_csv("../data/combined_full.csv")
print(df.shape)
for row in df.iterrows():
    print(len(row))

for keys in df.keys():
    if len(df[keys]) != 2236:
        print(keys)
'''
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

matches_kept = [100,99.5, 98.3, 97, 96, 94.3, 92.5, 90.5,86.0,75.3, 53.4, 16.9]
threshold = [0,1,2,3,4,5,6,7,8,9,10,11]

plt.plot(threshold, matches_kept)
plt.xticks(range(12))
plt.yticks(np.arange(0,110,10))
plt.xlabel("Player threshold")
plt.ylabel("Matches kept (%)")
plt.title("Retained matches")
plt.tight_layout()
plt.show()


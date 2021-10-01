import re
import pandas as pd

df = pd.read_csv("data/fd_gd_dup2.csv", sep=",", encoding="utf-8")
df.drop_duplicates(subset=None, inplace=True)
df.to_csv("fd_gd.csv", index=False)
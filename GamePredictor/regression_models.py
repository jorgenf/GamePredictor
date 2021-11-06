from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from GamePredictor import data
import time
from multiprocessing import Pool
import os


cm = 1/2.54
plt.rc('axes', titlesize=10)
plt.rc('axes', labelsize=10)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('figure', titlesize=14)
plt.rcParams['figure.figsize'] = (15*cm, 8*cm)

def logistic_regression(df, normalized = True, split=0.8):
    df = df.sample(frac=1, ignore_index=True)
    scores = df.iloc[:,:2]
    df = df.iloc[:, 2:]
    y = []
    for row, val in scores.iterrows():
        h = val["home_score"]
        a = val["away_score"]
        if h > a:
            y.append(1)
        elif a > h:
            y.append(-1)
        else:
            y.append(0)
    if normalized:
        min_max_scaler = preprocessing.MinMaxScaler()
        df = pd.DataFrame(min_max_scaler.fit_transform(df), columns=df.columns)

    train_x = df.iloc[0:round(df.shape[0]*split),3:]
    train_y = y[0:round(len(y)*split)]
    test_x = df.iloc[round(df.shape[0]*split):,3:]
    test_y = y[round(len(y)*split):]
    reg = LogisticRegression(max_iter=10000).fit(train_x,train_y)
    return reg.score(test_x,test_y)


if __name__ == '__main__':
    result = [[] for _ in range(12)]

    n = 20
    for dset in range(12):
        df = pd.read_csv(f"../data/combined_th{dset}.csv", index_col=False)
        df = data.simple_imputation(df)
        with Pool(os.cpu_count() - 1) as p:
            res = p.map(logistic_regression, [df for _ in range(n)])
            result[dset] = res
        print(result)
    plt.boxplot(result, showmeans=True)
    plt.title("Accuracy per threshold value")
    plt.ylabel("Accuracy")
    plt.xlabel("Minimum players found threshold")
    plt.xticks(range(12))
    plt.tight_layout()
    plt.show()

'''
result = 0
for i in range(20):
    res = logistic_regression(pd.read_csv("../data/combined_th11.csv"))
    result += res
print(result/20)
'''

'''
for i in range(8):
    result = []
    for data in ["../data/combined_full_mean_imp.csv", "../data/combined_full_median_imp.csv", "../data/combined_full_mostfrequent_imp.csv"]:
        result.append(logistic_regression(data, 0.8))
    print(result)

sum = 0
for i in range(100):
    result = logistic_regression(0.8)
    sum += result
    
avg = sum/100
print(avg)
'''
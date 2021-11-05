from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np

def logistic_regression(data, split):
    df = pd.read_csv(data, index_col=False)
    df = df.sample(frac=1, ignore_index=True)
    scores = df.iloc[:,:2]
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
    train_x = df.iloc[0:round(df.shape[0]*split),3:]
    train_y = y[0:round(len(y)*split)]
    test_x = df.iloc[round(df.shape[0]*split):,3:]
    test_y = y[round(len(y)*split):]
    reg = LogisticRegression(max_iter=10).fit(train_x,train_y)
    return reg.score(test_x,test_y)
result = 0
for i in range(20):
    result += logistic_regression("../data/combined_th11.csv", 0.8)
print(f"Result is: {result/20}")
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
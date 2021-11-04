import itertools
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from collections import Counter
from multiprocessing import Pool
import os
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import unicodedata

sns.set()
cm = 1/2.54
plt.rc('axes', titlesize=10)
plt.rc('axes', labelsize=10)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('figure', titlesize=14)
plt.rcParams['figure.figsize'] = (15*cm, 8*cm)

N_PLAYER_THRESHOLD = 8
data_path = "../data/"

def combine_data_avg(g=data_path + "game_data_ascii.csv", p=data_path + "player_data_ascii.csv", npth = N_PLAYER_THRESHOLD, years=[]):
    games = pd.read_csv(g, index_col=False)
    gk = games.keys().values
    if years:
        g = pd.DataFrame(columns=gk)
        for year in years:
            g = g.append(games[(games["date"].str.contains(year))])
        games = g
        games = games.reset_index(drop=True)
    players = pd.read_csv(p)
    pk = players.keys()[4:-16].values
    p_found = set()
    p_not_found = set()
    n_games = len(games)
    dropped = 0
    print(f"Total number of games: {n_games}")
    for i,s in games.iterrows():
        prog = (i / n_games) * 100
        print("\r |" + "#" * int(prog) + f"  {round(prog, 1) if i < n_games - 1 else 100}%| Game: {i}", end="")
        h_t = s["home_lineup"].split(",")
        a_t = s["away_lineup"].split(",")
        h_avg = np.zeros(len(pk))
        hn = 0
        a_avg = np.zeros(len(pk))
        an = 0
        for hp,ap in zip(h_t,a_t):
            hp = hp.lstrip()
            ap = ap.lstrip()
            hplayer = get_player(hp, players)
            if len(hplayer) == 0:
                p_not_found.add(hp)
            else:
                hatt = hplayer[pk].values[0]
                h_avg += hatt
                hn += 1
                p_found.add(hp)
            aplayer = get_player(ap, players)
            if len(aplayer) == 0:
                p_not_found.add(ap)
            else:
                aatt = aplayer[pk].values[0]
                a_avg += aatt
                an += 1
                p_found.add(ap)
        if hn < npth or an < npth:
            games = games.drop(index=i)
            dropped += 1
        else:
            h_avg /= hn
            h_avg = [round(x,1) for x in h_avg]
            a_avg /= an
            a_avg = [round(x, 1) for x in a_avg]
            games.at[i,"home_lineup"] = str(h_avg)
            games.at[i,"away_lineup"] = str(a_avg)
    games = games.reset_index(drop=True)
    print(f"Players found: {len(p_found)}")
    print(f"Players not found: {len(p_not_found)}")
    print(f"Players found: {round(len(p_found)/(len(p_found)+len(p_not_found))*100,1)}%")
    print(f"Matches dropped: {dropped}")
    print(f"Matches kept: {len(games)}")
    print(f"Matches kept: {round(len(games)/(len(games)+dropped)*100,1)}%")
    return games


def combine_data_full(g=data_path + "game_data_ascii.csv", p=data_path + "player_data_ascii.csv", years=[]):
    games = pd.read_csv(g, index_col=False)
    gk = games.keys().values
    if years:
        g = pd.DataFrame(columns=gk)
        for year in years:
            g = g.append(games[(games["date"].str.contains(year))])
        games = g
        games = games.reset_index(drop=True)
    players = pd.read_csv(p)
    pk = players.keys()[4:-16].values


    p_found = set()
    p_not_found = set()
    n_games = len(games)

    games_copy = games.copy(deep=True)
    new_columns = {}
    for team in ["H", "A"]:
        for player in range(1, 12):
            for attribute in pk:
                new_columns[f"{attribute}{team}{player}"] = []
    print(f"Total number of games: {n_games}")
    for i,s in games_copy.iterrows():
        prog = (i / n_games) * 100
        print("\r |" + "#" * int(prog) + f"  {round(prog, 1) if i < n_games - 1 else 100}%| Game: {i}", end="")
        h_t = s["home_lineup"].split(",")
        a_t = s["away_lineup"].split(",")


        for hp,ap, i in zip(h_t,a_t,range(1,12)):
            hp = hp.lstrip()
            ap = ap.lstrip()
            hplayer = get_player(hp, players)
            if len(hplayer) == 0:
                p_not_found.add(hp)
                for key in pk:
                    new_columns[f"{key}H{i}"].append(np.nan)
            else:
                hp_att = hplayer[pk].values[0]
                p_found.add(hp)
                for attribute, key in zip(hp_att, pk):
                    new_columns[f"{key}H{i}"].append(attribute)
            aplayer = get_player(ap, players)
            if len(aplayer) == 0:
                p_not_found.add(ap)
                for key in pk:
                    new_columns[f"{key}A{i}"].append(np.nan)
            else:
                ap_att = aplayer[pk].values[0]
                for attribute, key in zip(ap_att, pk):
                    new_columns[f"{key}A{i}"].append(attribute)
                p_found.add(ap)

    for key in new_columns.keys():
        games_copy[key] = new_columns[key]

    games_copy = games_copy.reset_index(drop=True)
    print(f"\nPlayers found: {len(p_found)}")
    print(f"Players not found: {len(p_not_found)}")
    print(f"Percentage players found: {round(len(p_found)/(len(p_found)+len(p_not_found))*100,1)}%")
    return games_copy


def get_player(name, df):
    return df.loc[df["Name"] == name]

def get_stats(data):
    df = pd.read_csv(data)
    cols = df.keys()[4:]
    stats = {}
    for key in cols:
        if key in ["Age", "Weight", "Height"]:
            nz = df[key].values.nonzero()
            col = df[key].iloc[nz]
        else:
            col = df[key]
        if type(col[0]) in [np.int, np.float, np.int64]:
            stats[f"{key}"] = {"maks": np.max(col), "min": np.min(col),  "mean": round(np.mean(col),2), "std": round(np.std(col),2)}
            plt.hist(col, bins=np.arange(col.min(), col.max()+1))
            plt.title(f"{key}")
            #plt.show()
    return stats


def plot_correlation(feature1, feature2, dataset):
    df = pd.read_csv(dataset)
    f1 = df[feature1].tolist()
    f2 = df[feature2].tolist()
    if df[feature1].dtype == object or df[feature2].dtype == object:
        return None
    data = Counter(zip(f1,f2))
    s = [0.5*data[(xx,yy)] for xx,yy in zip(f1,f2)]
    plt.title("Feature correlation")
    try:
        plt.scatter(f1, f2, c=s, cmap="Reds")
    except Exception:
        print("F1:")
        print(f1)
        print("F2:")
        print(f2)
        print("S:")
        print(s)
        raise Exception("Oh no!")

    plt.xticks(range(min(f1),max(f1) + 1, max(int(max(f1)/20),1)))
    plt.yticks(range(min(f2), max(f2) + 1, max(int(max(f2)/20),1)))

    plt.xlabel(feature1)
    plt.ylabel(feature2)
    plt.savefig(f"../Plots/FeatureCorrelations/{feature1}{feature2}")
    plt.clf()




def plot_histogram(feature, dataset):
    df = pd.read_csv(dataset)
    f = df[feature]
    if f.dtype == object:
        return None
    count = Counter(f)
    srt = sorted(count.items(), key=lambda x: x[0])
    feature_val = [x[0] for x in srt]
    feature_occurance = [x[1] for x in srt]
    plt.bar(x=feature_val, height=feature_occurance)
    plt.xticks(range(min(f),max(f)+1, max(int(max(f)/20),1)))
    plt.ylabel("Count")
    plt.xlabel("Feature value")
    plt.title(feature)

    plt.savefig(f"../Plots/Histograms/{feature}")
    plt.clf()


def run_mt_plots():
    if __name__ == "__main__":
        dataset = "../data/player_data.csv"
        df = pd.read_csv(dataset)
        hist_data = []
        corr_data = []
        for f1 in df.keys()[4:]:
            hist_data.append((f1, dataset))
            for f2 in df.keys()[5:]:
                corr_data.append((f1,f2,dataset))
        with Pool(os.cpu_count() - 1) as p:
            p.starmap(plot_histogram, hist_data)
            p.starmap(plot_correlation, corr_data)
            p.close()


def get_correlations():
    df = pd.read_csv("../data/player_data.csv")
    keys = df.keys()[4:]
    keys = keys.drop('PositionsDesc')
    comb = list(itertools.combinations(keys, 2))
    comb = [(x[0],x[1]) for x in comb if x[0] != x[1]]
    l = {}
    for c in comb:
        l[f"{c[0]}-{c[1]}"] = np.corrcoef(df[c[0]], df[c[1]])[0][1]
    print(sorted(l.items(), key = lambda kv:(kv[1], kv[0])))
    print(f"Mean correlation values: {sum(l.values())/len(l.values())}")
    print(f"Mean of positive correlations: {np.mean([x for x in l.values() if x >= 0])}")
    print(f"STD of positive correlations: {np.std([x for x in l.values() if x >= 0])}")
    print(f"Mean of negative correlations: {np.mean([x for x in l.values() if x <= 0])}")
    print(f"STD of negative correlations: {np.std([x for x in l.values() if x <= 0])}")
    print(f"Standard deviation: {np.std(list(l.values()))}")


combined_full = combine_data_full()
combined_full.drop(labels=[])
combined_full.to_csv("../data/combined_full.csv", na_rep='NULL', index=False)
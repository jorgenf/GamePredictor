from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
sns.set()

N_PLAYER_THRESHOLD = 8



def combine_data(g="data_clean.csv", p="player_data.csv", npth = N_PLAYER_THRESHOLD, years=[]):
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
            hplayer = get_player(hp,players)
            if len(hplayer) == 0:
                p_not_found.add(hp)
            else:
                hatt = hplayer[pk].values[0]
                h_avg += hatt
                hn += 1
                p_found.add(hp)
            aplayer = get_player(ap,players)
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
            stats[f"{key}"] = {"std": round(np.std(col),2), "mean": round(np.mean(col),2), "maks": np.max(col), "min": np.min(col)}
            plt.hist(col, bins=np.arange(col.min(), col.max()+1))
            plt.title(f"{key}")
            plt.show()
    return stats


print(get_stats("data/player_data.csv"))
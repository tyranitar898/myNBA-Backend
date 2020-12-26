from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import boxscorematchups
from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
import json
import time
import os
import ast
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
import numpy as np
from flask import Flask, request, jsonify
import matplotlib.pyplot as plt

active_players = players.get_inactive_players() + players.get_active_players()
# active_players = players.get_active_players()


def generatePlayerCarrerStat():
    f = open("stattt.txt", "a")
    for player in active_players:
        id = player['id']

        time.sleep(0.5)
        player_info = playercareerstats.PlayerCareerStats(
            player_id=id, timeout=1000)
        player_reg_stat = player_info.career_totals_regular_season.get_dict()
        player_stat = {"player": player,
                       "reg_season_career_total": player_reg_stat}
        print(player_reg_stat)
        f.write(str(player_stat) + "\n")


#{"name": "FG_PCT", "index": 8}, {"name": "FG3_PCT", "index": 11},
# features = [{"name": "FG3M", "index": 9},{"name": "REB", "index": 17}, {
       # "name": "AST", "index": 18}, {"name": "STL", "index": 19}, {"name": "BLK", "index": 20}, {"name": "TOV", "index": 21}, {"name": "PTS", "index": 23}]

def generateData(fileName):
    features = [{"name": "FG3M", "index": 9},{"name": "REB", "index": 17}, {
        "name": "AST", "index": 18}, {"name": "STL", "index": 19}, {"name": "BLK", "index": 20}]
    X = []
    Xlabels = []
    with open(fileName) as f:
        content = f.readlines()
    for line in content:
        playerDict = ast.literal_eval(line)
        name = playerDict['player']['full_name']
        dataarr = player_minute = playerDict["reg_season_career_total"]['data']
        
        if (len(dataarr) != 0 and len(dataarr[0]) != 0):
            # Minutes more than 4000 players   minute index = 5
            player_minute = playerDict["reg_season_career_total"]['data'][0][5]
            player_gamesplayed = playerDict["reg_season_career_total"]['data'][0][3]
            # print(player_minute, player_gamesplayed)
            if None not in playerDict["reg_season_career_total"]['data'][0]:
                if player_minute > 2000:
                    raw_stat_arr_for_player = playerDict["reg_season_career_total"]['data']

                    if len(raw_stat_arr_for_player) != 0:
                        raw_stat_arr_for_player = raw_stat_arr_for_player[0]

                    # print(name, raw_stat_arr_for_player)

                    thisplayerFeaturesArr = []
                    for feature in features:
                        featureValue = raw_stat_arr_for_player[feature['index']
                                                            ] / player_gamesplayed
                        thisplayerFeaturesArr.append(featureValue)

                    # FG_PCT = raw_stat_arr_for_player[8]
                    # FG3_PCT = raw_stat_arr_for_player[11]
                    # thisplayerFeaturesArr.append(FG_PCT)
                    # thisplayerFeaturesArr.append(FG3_PCT)
                    X.append(thisplayerFeaturesArr)
                    Xlabels.append(name)
    return X, Xlabels


def KMmeans_pred(n, fileNameStr):
    X, Xlabels = generateData('./data/' + fileNameStr)
    kmeans = KMeans(n, random_state=0)
    labels = kmeans.fit(X).predict(X)
    pred = []
    for i in range(len(labels)):
        # pred.append((labels[i], Xlabels[i]))
        pred.append({"class": int(labels[i]),"name": Xlabels[i]})
    return pred


def GMM_pred(n, fileNameStr):
    #  activePlayerCareerRegSeasonStats.txt  allPlayerCareerRegSeasonStats.txt
    X, Xlabels = generateData('./data/' + fileNameStr)
    gmm = GaussianMixture(n_components=n).fit(X)
    labels = gmm.predict(X)
    pred = []
    for i in range(len(labels)):
        # pred[Xlabels[i]] = labels[i]
        pred.append({"class": int(labels[i]),"name": Xlabels[i]})
    return pred


# # generatePlayerCarrerStat()
# pred = GMM_pred(20, "activePlayerCareerRegSeasonStats.txt")
# sorted_pred = dict(sorted(pred.items(), key=lambda item: item[1]))
# y = json.dumps(sorted_pred)


# init app
app = Flask("MYNBA")

@app.route('/', methods=['GET'])
def get():
    pred = GMM_pred(20, "activePlayerCareerRegSeasonStats.txt")
    sorted_pred = sorted(pred, key=lambda k: k["class"]) 
    return jsonify(sorted_pred)
    

#Run Server
if __name__ == "__main__":
    app.run()

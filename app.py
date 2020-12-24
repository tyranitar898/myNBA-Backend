from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import boxscorematchups
from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
import time
import os
import ast
from sklearn.cluster import KMeans
import numpy as np
from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
active_players = players.get_active_players()


#{"name": "FG_PCT", "index": 8}, {"name": "FG3_PCT", "index": 11},


def generateData():
    features = [{"name": "REB", "index": 17}, {
        "name": "AST", "index": 18}, {"name": "STL", "index": 19}, {"name": "PTS", "index": 23}]
    X = []
    Xlabels = []
    with open('playCareerRegSeasonStats.txt') as f:
        content = f.readlines()
    for line in content:
        dict = ast.literal_eval(line)
        name = dict['player']['full_name']
        dataarr = player_minute = dict["reg_season_career_total"]['data']
        if (len(dataarr) != 0):
            # Minutes more than 4000 players   minute index = 5
            player_minute = dict["reg_season_career_total"]['data'][0][5]
            player_gamesplayed = dict["reg_season_career_total"]['data'][0][3]

            if player_minute > 4000:
                raw_stat_arr_for_player = dict["reg_season_career_total"]['data']

                if len(raw_stat_arr_for_player) != 0:
                    raw_stat_arr_for_player = raw_stat_arr_for_player[0]

                # print(name, raw_stat_arr_for_player)

                thisplayerFeaturesArr = []
                for feature in features:
                    featureValue = raw_stat_arr_for_player[feature['index']
                                                           ] / player_gamesplayed
                    thisplayerFeaturesArr.append(featureValue)

                FG_PCT = raw_stat_arr_for_player[8]
                FG3_PCT = raw_stat_arr_for_player[11]
                thisplayerFeaturesArr.append(FG_PCT)
                thisplayerFeaturesArr.append(FG3_PCT)
                X.append(thisplayerFeaturesArr)
                Xlabels.append(name)
    return X, Xlabels


X, Xlabels= generateData()
kmeans = KMeans(5, random_state = 0)
labels = kmeans.fit(X).predict(X)
# print(labels)
# print(Xlabels)
for i in range(len(labels)):
    print(labels[i], Xlabels[i])


# for line in content:
#     print()

# with open('playerGameLog.txt') as f:
#     content = f.read()
# arr = (content.split('{'))

# f = open('playergamelog.txt', "a")
# i = 0
# for player in active_players:
#     id = player['id']
#     i +=1
#     time.sleep(2)
#     info = playergamelog.PlayerGameLog(player_id=id, season=2019)
#     x = info.player_game_log.get_data_frame()

#     print(i/len(active_players), str(player))
#     f.write(str(player)+"\n")
#     f.write(x.to_csv(index=False))

# f = open('stat.txt', "w")
# info = leaguegamelog.LeagueGameLog(player_or_team_abbreviation="P", season=2020)
# x = info.league_game_log.get_data_frame()

# print(x)
# for index, row in x.iterrows():
#     print(row["GAME_ID"])

# for player in active_players:
#     id = player['id']

#     time.sleep(0.5)

# player_info = playercareerstats.PlayerCareerStats(player_id=id, timeout=1000)
# player_reg_stat = player_info.career_totals_regular_season.get_dict()
# player_stat = {"player": player, "reg_season_career_total" : player_reg_stat}
# print(player_reg_stat)
# # f.write(str(player_stat) + "\n")

# init app
# app = Flask("MYNBA")

# @app.route('/', methods=['GET'])
# def get():
#     bron = [player for player in player_dict if player['full_name'] == 'LeBron James'][0]
#     bron_id = bron['id']

#     return jsonify(bron)

# #Run Server
# if __name__ == "__main__":
#     app.run(debug=True)

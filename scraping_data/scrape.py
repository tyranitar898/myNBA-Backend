from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import boxscorematchups
from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
import time
import os
import ast
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
import numpy as np
from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
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
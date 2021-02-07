from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import boxscorematchups
from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.endpoints import playercareerstats
# change api ---
from nba_api.stats.endpoints import playerprofilev2
#
from nba_api.stats.static import players
import json
import time
import os
import ast
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
import numpy as np
from flask import Flask, request, jsonify

# active_players = players.get_inactive_players() + players.get_active_players()
active_players = players.get_active_players()


def generateStats():
    #modify here
    f = open("PlayerRegSeasonStatBySeason.txt", "a")
    #---
    i=0
    for player in active_players:
        i +=1
        id = player['id']

        time.sleep(0.5)
        #modify here
        player_info = playerprofilev2.PlayerProfileV2(
            player_id=id, timeout=1000)
        player_reg_stat = player_info.season_totals_regular_season.get_dict()
        # ---
        player_stat = {"player_info": player,
                       "stats_per_season": player_reg_stat}
        # print(player_reg_stat)
        print(i/len(active_players))
        f.write(str(player_stat) + "\n")

generateStats()
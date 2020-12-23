from flask import Flask, request, jsonify

import os
import time
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

active_players = players.get_active_players()

# f = open('stat.txt', "w")


for player in active_players:
    id = player['id']
   
    time.sleep(0.5)
    player_info = playercareerstats.PlayerCareerStats(player_id=id, timeout=1000)
    player_reg_stat = player_info.career_totals_regular_season.get_dict()
    player_stat = {"player": player, "reg_season_career_total" : player_reg_stat}
    print(player_reg_stat)
    # f.write(str(player_stat) + "\n")
    





# #init app
# app = Flask("MYNBA")

# @app.route('/', methods=['GET'])
# def get():
#     bron = [player for player in player_dict if player['full_name'] == 'LeBron James'][0]
#     bron_id = bron['id']
    
#     return jsonify(bron)

# #Run Server
# if __name__ == "__main__":
#     app.run(debug=True) 